#!/bin/bash

# Stop all running containers
CONTAINER_IDS=$(sudo docker ps -aq)
if [ -n "$CONTAINER_IDS" ]; then
  sudo docker stop $CONTAINER_IDS
  sudo docker rm $CONTAINER_IDS
else
  echo "No containers to stop and remove"
fi

# Remove all images
IMAGE_IDS=$(sudo docker images -q)
if [ -n "$IMAGE_IDS" ]; then
  sudo docker rmi -f $IMAGE_IDS
else
  echo "No images to remove"
fi
