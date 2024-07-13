#!/bin/bash

# Set variables
NAMESPACE="frontend"

# Function to log messages with timestamps
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

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
configs=("namespace-frontend.yaml" "cluster-issuer.yaml" "certificate.yaml" "metallb-config.yaml" "react-frontend-deployment.yaml" "react-frontend-service.yaml" "react-ingress.yaml")

for config in "${configs[@]}"; do
  apply_config "/home/sellinios/aethra/microk8s/$config"
done

# Verify deployment
log "Verifying deployment..."
microk8s kubectl get pods -n $NAMESPACE
microk8s kubectl get svc -n $NAMESPACE
microk8s kubectl get ingress -n $NAMESPACE

log "Deployment completed!"
