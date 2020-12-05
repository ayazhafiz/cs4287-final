FROM ubuntu:18.04

RUN apt-get update && apt-get -y install \
  python3.6 \
  curl \
  python3-pip

WORKDIR /home/ubuntu
COPY . router/

RUN pip3 install Flask
RUN pip3 install -r router/requirements.txt

ENV ADDR_RUN_LANG_PY="docker.for.mac.localhost:9001"
ENV ADDR_RUN_LANG_JS="docker.for.mac.localhost:9002"
ENV ADDR_RUN_LANG_RUST="192.168.99.100:9003"
ENV ADDR_RUN_LANG_CPP="192.168.99.100:9004"

ENTRYPOINT ["waitress-serve", "--port=8000", "--call", "router:create_app"]
