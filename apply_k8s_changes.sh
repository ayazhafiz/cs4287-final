#!/bin/bash

set -euxo pipefail

git diff --name-only HEAD^ HEAD > changed_files.txt
while IFS= read -r file
do
  echo "Changed file: $file"
  if [[ $file == kubernetes/* && $file =~ ".yaml" ]]; then
    echo "Applying k8s changes in $file"
    kubectl apply -f $file
  fi

done < changed_files.txt
