FROM ubuntu:18.04

RUN apt-get update && apt-get -y install \
  python3.6 \
  curl \
  python3-pip

WORKDIR /home/ubuntu
COPY . router/

RUN pip3 install Flask
RUN pip3 install -r router/requirements.txt

ENTRYPOINT ["waitress-serve", "--port=8000", "--call", "router:create_app"]
