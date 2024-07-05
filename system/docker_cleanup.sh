#!/bin/bash

# Stop all running containers
CONTAINER_IDS=$(docker ps -aq)
if [ -n "$CONTAINER_IDS" ]; then
  docker stop $CONTAINER_IDS
else
  echo "No containers to stop"
fi

# Remove all containers
if [ -n "$CONTAINER_IDS" ]; then
  docker rm $CONTAINER_IDS
else
  echo "No containers to remove"
fi

# Remove all images
IMAGE_IDS=$(docker images -q)
if [ -n "$IMAGE_IDS" ]; then
  docker rmi $IMAGE_IDS
else
  echo "No images to remove"
fi
