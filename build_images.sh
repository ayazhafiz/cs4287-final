#!/bin/bash

python3 images/imagegen.py

docker build -t runpython -f images/python/Dockerfile . &
docker build -t runjavascript -f images/javascript/Dockerfile . &
docker build -t runrust -f images/rust/Dockerfile . &
wait
