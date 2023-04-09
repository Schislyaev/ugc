#!/bin/bash

echo "Waiting for zookeeper..."
while ! nc -z $ZOO_HOST $ZOO_PORT; do
  sleep 0.1
done
echo "zookeeper started"