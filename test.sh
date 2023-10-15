#!/bin/bash
CONTAINER=sleepy_buck
RUNNING=$(docker ps --filter name=$CONTAINER | wc -l)
if [ $RUNNING -gt 1 ]; then
  sudo docker rm --force $CONTAINER
else
  echo "'$CONTAINER' does not exist."
fi