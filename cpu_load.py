# From https://github.com/GaetanoCarlucci/CPULoadGenerator

import multiprocessing

import sys
sys.path.insert(0, 'utils')

import os, psutil
import threading
import time

class closedLoopActuator():
    """
        Generates CPU load by tuning the sleep time
    """

    def __init__(self, controller, monitor, duration, cpu_core, target, plot):
        self.controller = controller
        self.monitor = monitor
        self.duration = duration
        self.plot = plot
        self.target = target
        self.controller.setCpu(self.monitor.getCpuLoad())
        self.period = 0.05  # actuation period  in seconds
        self.last_plot_time = time.time()
        self.start_time = time.time()
        if self.plot:
            print("no plots supported")

    def generate_load(self, sleep_time):
        interval = time.time() + self.cycle - sleep_time
        # generates some getCpuLoad for interval seconds
        while (time.time() < interval):
            pr = 213123  # generates some load
            pr * pr
            pr = pr + 1
        time.sleep(sleep_time)  # controller actuation

    def sendPlotSample(self):
        if self.plot:
            if (time.time() - self.last_plot_time) > 0.2:
                self.graph.plotSample(self.controller.getCpu(), self.controller.getCpuTarget() * 100)
                self.last_plot_time = time.time()

    def close(self):
        if self.plot:
            self.graph.close()

    def generate_load(self, sleep_time):
        interval = time.time() + self.period - sleep_time
        # generates some getCpuLoad for interval seconds
        while (time.time() < interval):
            pr = 213123  # generates some load
            pr * pr
            pr = pr + 1

        time.sleep(sleep_time)

    def run(self):
        while (time.time() - self.start_time) <= self.duration:
            self.controller.setCpu(self.monitor.getCpuLoad())
            sleep_time = self.controller.getSleepTime()
            self.generate_load(sleep_time)
            self.sendPlotSample()
        return sleep_time

    def run_sequence(self, sequence):
        for cpuTarget in sequence:
            stepPeriod = time.time() + 4
            self.controller.setCpuTarget(cpuTarget)
            self.monitor.setCPUTarget(cpuTarget)
            while (time.time() < stepPeriod):
                self.controller.setCpu(self.monitor.getCpuLoad())
                sleep_time = self.controller.getSleepTime()
                self.generate_load(sleep_time)
                self.monitor.setSleepTime(sleep_time)
                self.sendPlotSample()

class MonitorThread(threading.Thread):
    """
       Monitors the CPU status
    """
    def __init__(self, cpu_core, interval):
        self.sampling_interval = interval; # sample time interval
        self.sample = 0.5; # cpu load measurement sample
        self.cpu = 0.5; # cpu load filtered
        self.running = 1; # thread status
        self.alpha = 1; # filter coefficient
        self.sleepTimeTarget = 0.03
        self.sleepTime = 0.03
        self.cpuTarget = 0.5
        self.cpu_core = cpu_core
        self.dynamics = {"time":[], "cpu":[], "sleepTimeTarget":[], "cpuTarget":[],  "sleepTime":[],}
        super(MonitorThread, self).__init__()
        
    def getCpuLoad(self):
        return self.cpu

    def setSleepTimeTarget(self, sleepTimeTarget):
        self.sleepTimeTarget = sleepTimeTarget

    def setSleepTime(self, sleepTime):
        self.sleepTime = sleepTime

    def setCPUTarget(self, cpuTarget):
        self.cpuTarget = cpuTarget

    def getDynamics(self):
    	return self.dynamics
        
    def run(self):
        start_time = time.time()
        p = psutil.Process(os.getpid())
        try:
            p.set_cpu_affinity([self.cpu_core]) #the process is forced to run only on the selected CPU
        except AttributeError:
            p.cpu_affinity([self.cpu_core])
            
        while self.running:
            try:
                self.sample = p.get_cpu_percent(self.sampling_interval)
            except AttributeError:
                self.sample = p.cpu_percent(self.sampling_interval)
                
            self.cpu = self.alpha * self.sample + (1 - self.alpha)*self.cpu # first order filter on the measurement samples
            #self.cpu_log.append(self.cpu)
            self.dynamics['time'].append(time.time() - start_time)
            self.dynamics['cpu'].append(self.cpu)
            self.dynamics['sleepTimeTarget'].append(self.sleepTimeTarget)
            self.dynamics['sleepTime'].append(self.sleepTime)
            self.dynamics['cpuTarget'].append(self.cpuTarget)

class ControllerThread(threading.Thread):
    """
        Controls the CPU status
    """
    def __init__(self, interval, ki = None, kp = None):
        self.running = 1;  # thread status
        self.sampling_interval = interval
        self.period = 0.1 # actuation period  in seconds
        self.sleepTime = 0.02; # this is controller output: determines the sleep time to achieve the requested CPU load
        self.alpha = 0.2; # filter coefficient
        self.CT = 0.20;  # target CPU load should be provided as input 
        self.cpu = 0;   # current CPU load returned from the Monitor thread
        self.cpuPeriod = 0.03;
        if ki is None:
          self.ki = 0.2   # integral constant of th PI regulator 
        if kp is None:
          self.kp = 0.02  # proportional constant of th PI regulator
        self.int_err = 0;  # integral error
        self.last_ts = time.time();  # last sampled time
        super(ControllerThread, self).__init__()
        
    def getSleepTime(self):
        return self.sleepTime

    def cpu_model(self, cpu_period):
        sleepTime = self.period - cpu_period
        return sleepTime

    def getCpuTarget(self):
        return self.CT

    def setCpu(self, cpu): 
        self.cpu = self.alpha * cpu + (1 - self.alpha)*self.cpu # first order filter on the measurement samples

    def getCpu(self): 
        return self.cpu

    def setCpuTarget(self, CT): 
        self.CT = CT
     
    def run(self):
        while self.running:
            # ControllerThread has to have the same sampling interval as MonitorThread
            time.sleep(self.sampling_interval)
            self.err = self.CT - self.cpu*0.01  # computes the proportional error
            ts = time.time()
            
            samp_int = ts - self.last_ts  # sample interval 
            self.int_err = self.int_err + self.err*samp_int  # computes the integral error
            self.last_ts = ts
            self.cpuPeriod = self.kp*self.err  + self.ki*self.int_err

            #anti wind up control
            if self.cpuPeriod < 0:
                self.cpuPeriod = 0
                self.int_err = self.int_err - self.err*samp_int
            if self.cpuPeriod > self.period:
                self.cpuPeriod = self.period
                self.int_err = self.int_err - self.err*samp_int
            self.sleepTime = self.cpu_model(self.cpuPeriod)

option_cpuLoad = 0.4
option_duration = 20
option_plot = False
option_cpu_core = 0

monitor = MonitorThread(option_cpu_core, 0.1)
monitor.start()

control = ControllerThread(0.1)
control.start()
control.setCpuTarget(option_cpuLoad)

actuator = closedLoopActuator(control, monitor, option_duration, option_cpu_core, option_cpuLoad, option_plot)
actuator.run()
actuator.close()

monitor.running = 0;
control.running = 0;
monitor.join()
control.join()
