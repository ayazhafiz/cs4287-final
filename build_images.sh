#!/bin/bash

set -euo pipefail

PUSH="${PUSH-false}"
ORG="kevjin"

function build_image {
  image_path=$1
  dockerfile_path=$2

  docker build -t "$image_path:latest" \
    -f "$dockerfile_path" \
    --cache-from "$image_path" \
    .

  if [[ "$PUSH" == "true" ]]; then
    docker push "$image_path:latest"
  fi
}

built_images=""

git diff --name-only HEAD^ HEAD > changed_files.txt
while IFS= read -r file
do
  image_path=""
  dockerfile_path=""

  echo "Changed file: $file"
  for lang in runlang_base python javascript cpp rust; do
    # If the base image was modified, then rebuild all images
    if [[ $file == images/$lang/* || $file == images/runlang_base/* ]]; then
      if [[ "$built_images" =~ $lang ]]; then
        echo "$lang has already been built. Skipping $file"
        continue
      fi

      if [[ $lang == "runlang_base" ]]; then
        image_path="$ORG/$lang"
      else
        image_path="$ORG/run$lang"
      fi

      dockerfile_path="images/$lang/Dockerfile"
      built_images="$built_images $lang"

      echo "Building image: $image_path for filepath: $file"
      build_image $image_path $dockerfile_path
    fi
  done

done < changed_files.txt
