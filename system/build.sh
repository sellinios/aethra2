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

# Variables for frontend
FRONTEND_IMAGE_NAME=$DOCKER_HUB_USERNAME/frontend
FRONTEND_TAG=$(date +%Y%m%d%H%M%S)
FRONTEND_FULL_IMAGE_NAME=$FRONTEND_IMAGE_NAME:$FRONTEND_TAG

# Variables for backend
BACKEND_IMAGE_NAME=$DOCKER_HUB_USERNAME/backend
BACKEND_TAG=$(date +%Y%m%d%H%M%S)
BACKEND_FULL_IMAGE_NAME=$BACKEND_IMAGE_NAME:$BACKEND_TAG

# Navigate to the aethra directory
cd /home/sellinios/aethra || { echo "Directory /home/sellinios/aethra not found. Exiting."; exit 1; }

# Copy ads.txt into the frontend directory if it doesn't exist
if [ ! -f frontend/ads.txt ]; then
  cp ads/ads.txt frontend/
fi

# Build the frontend Docker image
cd frontend || { echo "Directory /home/sellinios/aethra/frontend not found. Exiting."; exit 1; }
sudo docker build -t $FRONTEND_FULL_IMAGE_NAME .
if [ $? -ne 0 ]; then
  echo "Docker build for frontend failed. Exiting."
  exit 1
fi

# Push the frontend Docker image to Docker Hub
sudo docker push $FRONTEND_FULL_IMAGE_NAME
if [ $? -ne 0 ]; then
  echo "Docker push for frontend failed. Exiting."
  exit 1
fi

# Build the backend Docker image
cd ../backend || { echo "Directory /home/sellinios/aethra/backend not found. Exiting."; exit 1; }
sudo docker build -t $BACKEND_FULL_IMAGE_NAME .
if [ $? -ne 0 ]; then
  echo "Docker build for backend failed. Exiting."
  exit 1
fi

# Push the backend Docker image to Docker Hub
sudo docker push $BACKEND_FULL_IMAGE_NAME
if [ $? -ne 0 ]; then
  echo "Docker push for backend failed. Exiting."
  exit 1
fi

# Update frontend-deployment.yaml and backend-deployment.yaml with the new image tags for frontend and backend
sed -i "s|image: $FRONTEND_IMAGE_NAME:.*|image: $FRONTEND_FULL_IMAGE_NAME|g" /home/sellinios/aethra/microk8s/frontend-deployment.yaml
sed -i "s|image: $BACKEND_IMAGE_NAME:.*|image: $BACKEND_FULL_IMAGE_NAME|g" /home/sellinios/aethra/microk8s/backend-deployment.yaml

if [ $? -ne 0 ]; then
  echo "Failed to update deployment files. Exiting."
  exit 1
fi

echo "Docker images built and pushed successfully. Deployment files updated."
