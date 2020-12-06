#!/bin/bash

set -euvo pipefail

PUSH="${PUSH-false}"
ORG="kevjin"

docker build -t "$ORG/runlang_base:latest" \
  -f "images/runlang_base/Dockerfile" \
  --cache-from "$ORG/runlang_base" \
  .

if [[ "$PUSH" == "true" ]]; then
  docker push "$ORG/runlang_base:latest"
fi

python3 images/imagegen.py

for lang in python javascript cpp rust; do
  dockerfile="images/$lang/Dockerfile"
  image="ayazhafiz/run$lang"
  docker build -t "$image:latest" \
    -f "$dockerfile" \
    --cache-from "$image" \
    .

  if [[ "$PUSH" == "true" ]]; then
    docker push "$image:latest"
  fi
done
