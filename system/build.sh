#!/bin/bash

# Docker Hub credentials
DOCKER_HUB_USERNAME="sellinios"
DOCKER_HUB_PASSWORD="faidra123!@#"

# Login to Docker Hub
echo "Logging in to Docker Hub..."
echo $DOCKER_HUB_PASSWORD | sudo docker login -u $DOCKER_HUB_USERNAME --password-stdin

# Check if login was successful
if [ $? -ne 0 ]; then
  echo "Docker login failed. Exiting."
  exit 1
fi

# Variables
IMAGE_NAME=$DOCKER_HUB_USERNAME/frontend
TAG=$(date +%Y%m%d%H%M%S)
FULL_IMAGE_NAME=$IMAGE_NAME:$TAG

# Navigate to the aethra directory
cd /home/sellinios/aethra || { echo "Directory /home/sellinios/aethra not found. Exiting."; exit 1; }

# Copy ads.txt into the frontend directory if it doesn't exist
if [ ! -f frontend/ads.txt ]; then
  cp ads/ads.txt frontend/
fi

# Navigate to the frontend directory
cd frontend || { echo "Directory /home/sellinios/aethra/frontend not found. Exiting."; exit 1; }

# Build the Docker image
sudo docker build -t $FULL_IMAGE_NAME .
if [ $? -ne 0 ]; then
  echo "Docker build failed. Exiting."
  exit 1
fi

# Push the Docker image to Docker Hub
sudo docker push $FULL_IMAGE_NAME
if [ $? -ne 0 ]; then
  echo "Docker push failed. Exiting."
  exit 1
fi

# Update deployment.yaml with the new image tag
sed -i "s|image: $IMAGE_NAME:.*|image: $FULL_IMAGE_NAME|g" /home/sellinios/aethra/microk8s/deployment.yaml
if [ $? -ne 0 ]; then
  echo "Failed to update deployment.yaml. Exiting."
  exit 1
fi

echo "Docker image pushed and deployment.yaml updated."
