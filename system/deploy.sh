#!/bin/bash

# Set variables
DOCKER_USERNAME="sellinios"
DOCKER_PASSWORD="your-docker-password"
IMAGE_NAME="react-app"
NAMESPACE="frontend"

# Step 1: Build the Docker image
echo "Building Docker image..."
if [ -d "../frontend" ]; then
  docker build -t $DOCKER_USERNAME/$IMAGE_NAME:latest ../frontend
else
  echo "Error: Directory ../frontend does not exist."
  exit 1
fi

# Step 2: Push the Docker image to Docker Hub
echo "Pushing Docker image to Docker Hub..."
echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
docker push $DOCKER_USERNAME/$IMAGE_NAME:latest

# Step 3: Apply Kubernetes configurations

# Check if the file exists before applying
apply_config() {
  if [ -f "$1" ]; then
    microk8s kubectl apply -f "$1"
  else
    echo "Error: File $1 does not exist."
    exit 1
  fi
}

# Create namespace
echo "Creating namespace..."
apply_config "../microk8s/namespace-frontend.yaml"

# Create cluster issuer
echo "Creating cluster issuer..."
apply_config "../microk8s/cluster-issuer.yaml"

# Create MetalLB config
echo "Creating MetalLB config..."
apply_config "../microk8s/metallb-config.yaml"

# Deploy the frontend application
echo "Deploying frontend application..."
apply_config "../microk8s/react-frontend-deployment.yaml"

# Create frontend service
echo "Creating frontend service..."
apply_config "../microk8s/react-frontend-service.yaml"

# Create ingress resource
echo "Creating ingress resource..."
apply_config "../microk8s/react-ingress.yaml"

# Ensure MetalLB is configured for LoadBalancer service
echo "Ensuring MetalLB is configured for LoadBalancer service..."
microk8s enable metallb

# Ensure Nginx Ingress controller is enabled
echo "Enabling Nginx Ingress controller..."
microk8s enable ingress

# Apply Nginx Ingress service
echo "Applying Nginx Ingress service..."
apply_config "../microk8s/nginx-ingress-service.yaml"

# Verify deployment
echo "Verifying deployment..."
microk8s kubectl get pods -n $NAMESPACE
microk8s kubectl get svc -n $NAMESPACE
microk8s kubectl get ingress -n $NAMESPACE
microk8s kubectl get pods -n ingress
microk8s kubectl get svc -n ingress

echo "Deployment completed!"
