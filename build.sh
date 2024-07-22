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
FRONTEND_TAG=latest  # Changed to 'latest' for simplicity
FRONTEND_FULL_IMAGE_NAME=$FRONTEND_IMAGE_NAME:$FRONTEND_TAG

# Variables for backend
BACKEND_IMAGE_NAME=$DOCKER_HUB_USERNAME/backend
BACKEND_TAG=latest  # Changed to 'latest' for simplicity
BACKEND_FULL_IMAGE_NAME=$BACKEND_IMAGE_NAME:$BACKEND_TAG

# Navigate to the aethra directory
cd /home/sellinios/aethra || { echo "Directory /home/sellinios/aethra not found. Exiting."; exit 1; }

# Copy ads.txt into the frontend directory if it doesn't exist
if [ ! -f frontend/ads.txt ]; then
  cp ads/ads.txt frontend/
fi

# Build the frontend Docker image
cd frontend || { echo "Directory /home/sellinios/aethra/frontend not found. Exiting."; exit 1; }
sudo docker build --no-cache -t $FRONTEND_FULL_IMAGE_NAME .
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
sudo docker build --no-cache -t $BACKEND_FULL_IMAGE_NAME .
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

# Apply Kubernetes configurations
echo "Applying Kubernetes configurations for frontend..."
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/frontend-namespace.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/frontend-deployment.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/frontend-service.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/frontend-ingress.yaml

if [ $? -ne 0 ]; then
  echo "Failed to apply frontend Kubernetes configurations. Exiting."
  exit 1
fi

echo "Applying Kubernetes configurations for backend..."
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/backend-namespace.yaml

echo "Applying ConfigMap and Secret for backend..."
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/configmap.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/django-secret.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/django-config.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/database-secret.yaml

if [ $? -ne 0 ]; then
  echo "Failed to apply ConfigMap or Secret. Exiting."
  exit 1
fi

microk8s kubectl apply -f /home/sellinios/aethra/microk8s/backend-deployment.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/backend-service.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/backend-ingress.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/postgres-deployment.yaml

if [ $? -ne 0 ]; then
  echo "Failed to apply backend Kubernetes configurations. Exiting."
  exit 1
fi

echo "Applying Kubernetes configurations for ingress..."
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/ingress-namespace.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/nginx-ingress-service.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/cluster-issuer.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/tls-certificate.yaml

if [ $? -ne 0 ]; then
  echo "Failed to apply ingress Kubernetes configurations. Exiting."
  exit 1
fi

echo "Docker images built, pushed, and Kubernetes configurations applied successfully."

# Get all resources in the frontend namespace
echo "Resources in frontend namespace:"
microk8s kubectl get all -n frontend

# Get all resources in the backend namespace
echo "Resources in backend namespace:"
microk8s kubectl get all -n backend

# Get all resources in the ingress namespace
echo "Resources in ingress namespace:"
microk8s kubectl get all -n ingress

echo "Code pulled, built, deployed, and old ReplicaSets cleaned up successfully."
