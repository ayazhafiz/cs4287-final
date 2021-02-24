import gzip
import ctypes
import time

from datetime import datetime

class Request(ctypes.BigEndianStructure):
    _fields_ = [
        ("timestamp", ctypes.c_uint32),
        ("clientID", ctypes.c_uint32),
        ("objectID", ctypes.c_uint32),
        ("size", ctypes.c_uint32),
        ("method", ctypes.c_uint8),
        ("status", ctypes.c_uint8),
        ("type", ctypes.c_uint8),
        ("server", ctypes.c_uint8),
    ]

def get_requests_per_second_interval(seconds):
    requests_per_sec_interval = [0]
    interval_start_timestamp = None
    # The dataset can be fetched from Internet Traffic Archive's World Cup (1988) traffic data.
    with gzip.open("ita_public_tools/input/wc_day25_1.gz", "rb") as f:
        result = []
        request = Request()
        while f.readinto(request) == ctypes.sizeof(request):
            ts = request.timestamp
            # Note: These timestamps are actually in GMT (+0200), but that doesn't
            # matter for the purpose of the load testing.
            date = datetime.fromtimestamp(ts)
            date_formatted = date.strftime('%A %B %d. %Y %H:%M:%S')
            # print(date_formatted)

            if interval_start_timestamp is None:
                interval_start_timestamp = ts

            while ts - interval_start_timestamp > seconds:
                interval_start_timestamp += seconds
                yield requests_per_sec_interval[-1]
                requests_per_sec_interval.append(0)

            requests_per_sec_interval[-1] += 1
