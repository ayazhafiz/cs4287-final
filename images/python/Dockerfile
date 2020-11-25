# Generated Dockerfile, do not modify directly!
# Modify `dockergen.yaml` and run
#   `python images/dockergen.py` in the root directory.
FROM ubuntu:18.04
SHELL ["/bin/bash", "-c"]

ENV RUN_LANG_UBUNTU="18.04"
ENV RUN_LANG_WHICH="python"
ENV RUN_LANG_WHICH_DESCRIPTION="python 3.7"

# Service setup
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get update && apt-get -y install sudo
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

RUN apt-get install -y python3.7 python3-pip
COPY run_lang/requirements.txt /tmp/requirements.txt
RUN pip3 install --requirement /tmp/requirements.txt

# Pre-install
RUN apt-get install -y python3.7 python3-pip

# Package install
RUN pip3 install numpy==1.19.4
RUN pip3 install pendulum==2.1.2
RUN pip3 install requests==2.25.0

# Post-install
RUN echo 0

# Service setup
COPY run_lang /run_lang
COPY start_run_lang.sh /start_run_lang.sh
COPY images/python/packages /packages

WORKDIR /

CMD ["./start_run_lang.sh"]
