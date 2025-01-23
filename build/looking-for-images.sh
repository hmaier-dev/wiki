#!/usr/bin/env bash

images=$(grep -Eo "FROM\s([a-zA-Z]+.+)" "./Earthfile" | awk '{ match($0, /FROM\s([a-zA-Z]+.+)/, arr); print arr[1] }')

for image in $images; do
  docker pull $image
done;

