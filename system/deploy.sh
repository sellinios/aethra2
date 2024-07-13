#!/bin/bash

# Set variables
NAMESPACE="frontend"
INGRESS_NAMESPACE="ingress"

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

# Function to wait for pods to be in a Running state
wait_for_pods() {
  local namespace=$1
  while true; do
    local pending=$(microk8s kubectl get pods -n $namespace --field-selector=status.phase!=Running | wc -l)
    if [ $pending -le 1 ]; then
      break
    fi
    log "Waiting for all pods to be in Running state in namespace $namespace..."
    sleep 5
  done
}

# Apply Kubernetes configurations
log "Applying Kubernetes configurations..."
configs=("namespace.yaml" "cluster-issuer.yaml" "certificate.yaml" "metallb-config.yaml" "deployment.yaml" "service.yaml" "ingress.yaml" "nginx-ingress-service.yaml")

for config in "${configs[@]}"; do
  apply_config "/home/sellinios/aethra/microk8s/$config"
done

# Wait for all pods to be running
wait_for_pods $NAMESPACE
wait_for_pods $INGRESS_NAMESPACE

# Verify deployment
log "Verifying deployment..."
microk8s kubectl get pods -n $NAMESPACE
microk8s kubectl get svc -n $NAMESPACE
microk8s kubectl get ingress -n $NAMESPACE
microk8s kubectl get svc -n $INGRESS_NAMESPACE

# Verify Ingress IP and status
log "Checking Ingress status..."
INGRESS_IP=$(microk8s kubectl get ingress frontend-ingress -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
if [ -z "$INGRESS_IP" ]; then
  log "Error: Ingress does not have an external IP."
  exit 1
else
  log "Ingress external IP: $INGRESS_IP"
fi

# Check the status of the nginx ingress service
log "Checking nginx ingress service status..."
NGINX_SERVICE_IP=$(microk8s kubectl get svc nginx-ingress-microk8s-controller -n $INGRESS_NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
if [ -z "$NGINX_SERVICE_IP" ]; then
  log "Error: nginx ingress service does not have an external IP."
  exit 1
else
  log "nginx ingress service external IP: $NGINX_SERVICE_IP"
fi

log "Deployment completed!"
