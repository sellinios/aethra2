#!/bin/bash

# Ensure the script is run with superuser privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or with sudo."
  exit 1
fi

# Stop and remove all containers
echo "Stopping all running containers..."
CONTAINER_IDS=$(docker ps -aq)
if [ -n "$CONTAINER_IDS" ]; then
  docker stop $CONTAINER_IDS
  echo "Removing all containers..."
  docker rm $CONTAINER_IDS
else
  echo "No containers to stop and remove."
fi

# Remove all images
echo "Removing all Docker images..."
IMAGE_IDS=$(docker images -q)
if [ -n "$IMAGE_IDS" ]; then
  docker rmi -f $IMAGE_IDS
else
  echo "No images to remove."
fi

# Optional: Remove unused volumes and networks
echo "Removing unused volumes and networks..."
docker volume prune -f
docker network prune -f

# Clean up build cache (optional)
echo "Removing build cache..."
docker builder prune -f

echo "Cleanup complete."
