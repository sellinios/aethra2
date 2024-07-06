#!/bin/bash

# Define variables
DOCKER_IMAGE_NAME="sellinios/react-frontend:latest"
NAMESPACE="kairos"

# Docker login
sudo docker login -u sellinios -p "faidra123!@#"

# Build the Docker image
sudo docker build -t $DOCKER_IMAGE_NAME ./frontend || { echo "Docker build failed"; exit 1; }

# Push the Docker image to Docker Hub
sudo docker push $DOCKER_IMAGE_NAME || { echo "Docker push failed"; exit 1; }

# Apply the Kubernetes namespace
microk8s kubectl apply -f ~/aethra/k8s/namespace-kairos.yaml || { echo "Failed to apply namespace"; exit 1; }

# Apply the Kubernetes deployment
microk8s kubectl apply -f ~/aethra/k8s/react-frontend-deployment.yaml || { echo "Failed to apply deployment"; exit 1; }

# Apply the Kubernetes service
microk8s kubectl apply -f ~/aethra/k8s/react-frontend-service.yaml || { echo "Failed to apply service"; exit 1; }

# Apply the Kubernetes ingress
microk8s kubectl apply -f ~/aethra/k8s/ingress.yaml || { echo "Failed to apply ingress"; exit 1; }

# Get the status of pods
microk8s kubectl get pods -n $NAMESPACE
