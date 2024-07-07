#!/bin/bash

# Set variables
DOCKER_USERNAME="sellinios"
DOCKER_PASSWORD="faidra123!@#"
IMAGE_NAME="react-app"
NAMESPACE="frontend"

# Function to log messages with timestamps
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Step 1: Enable necessary MicroK8s addons
log "Enabling necessary MicroK8s addons..."
microk8s enable dns dashboard storage ingress cert-manager metrics-server

# Step 2: Docker login
log "Logging into Docker..."
echo $DOCKER_PASSWORD | sudo docker login -u $DOCKER_USERNAME --password-stdin || { log "Error: Docker login failed."; exit 1; }

# Step 3: Build the Docker image
log "Building Docker image..."
if [ -d "../frontend" ]; then
  sudo docker build -t $DOCKER_USERNAME/$IMAGE_NAME:latest ../frontend || { log "Error: Docker build failed."; exit 1; }
else
  log "Error: Directory ../frontend does not exist."
  exit 1
fi

# Step 4: Push the Docker image to Docker Hub
log "Pushing Docker image to Docker Hub..."
sudo docker push $DOCKER_USERNAME/$IMAGE_NAME:latest || { log "Error: Docker push failed."; exit 1; }

# Function to apply Kubernetes configurations
apply_config() {
  if [ -f "$1" ]; then
    microk8s kubectl apply -f "$1" || { log "Error: Failed to apply $1"; exit 1; }
  else
    log "Error: File $1 does not exist."
    exit 1
  fi
}

# Step 5: Apply Kubernetes configurations
log "Applying Kubernetes configurations..."
apply_config "../microk8s/namespace-frontend.yaml"
apply_config "../microk8s/cluster-issuer.yaml"
apply_config "../microk8s/certificate.yaml"

# Ensure metallb-system namespace exists
log "Ensuring metallb-system namespace exists..."
microk8s kubectl create namespace metallb-system --dry-run=client -o yaml | microk8s kubectl apply -f -

# Apply MetalLB config
apply_config "../microk8s/metallb-config.yaml"
apply_config "../microk8s/react-frontend-deployment.yaml"
apply_config "../microk8s/react-frontend-service.yaml"
apply_config "../microk8s/nginx-ingress-service.yaml"
apply_config "../microk8s/react-ingress.yaml"

# Step 6: Ensure MetalLB is configured for LoadBalancer service
log "Ensuring MetalLB is configured for LoadBalancer service..."
echo "65.109.117.111-65.109.117.111" | sudo microk8s enable metallb

# Step 7: Ensure Nginx Ingress controller is enabled
log "Enabling Nginx Ingress controller..."
sudo microk8s enable ingress

# Step 8: Create Docker registry secret
log "Creating Docker registry secret..."
sudo microk8s kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=$DOCKER_USERNAME \
  --docker-password=$DOCKER_PASSWORD \
  --docker-email=lefteris.broker@gmail.com \
  -n $NAMESPACE --dry-run=client -o yaml | sudo microk8s kubectl apply -f -

# Verify deployment
log "Verifying deployment..."
microk8s kubectl get pods -n $NAMESPACE
microk8s kubectl get svc -n $NAMESPACE
microk8s kubectl get ingress -n $NAMESPACE
microk8s kubectl get pods -n ingress
microk8s kubectl get svc -n ingress

log "Deployment completed!"
