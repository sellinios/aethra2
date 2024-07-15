#!/bin/bash

# Set variables
FRONTEND_NAMESPACE="frontend"
BACKEND_NAMESPACE="backend"
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

# Function to wait for pods to be in a Running state with a timeout
wait_for_pods() {
  local namespace=$1
  local timeout=$2
  local interval=5
  local waited=0

  while true; do
    local pending=$(microk8s kubectl get pods -n $namespace --field-selector=status.phase!=Running | wc -l)
    if [ $pending -le 1 ]; then
      break
    fi

    if [ $waited -ge $timeout ]; then
      log "Timeout waiting for pods to be in Running state in namespace $namespace."
      microk8s kubectl get pods -n $namespace
      exit 1
    fi

    log "Waiting for all pods to be in Running state in namespace $namespace..."
    sleep $interval
    waited=$((waited + interval))
  done
}

# Create Docker registry secret
microk8s kubectl create secret docker-registry dockerhub-secret \
    --docker-username=sellinios \
    --docker-password=faidra123!@# \
    --docker-email=lefteris.broker@gmail.com \
    --namespace frontend --dry-run=client -o yaml | microk8s kubectl apply -f -

# Apply Kubernetes configurations for frontend
log "Applying Kubernetes configurations for frontend..."
frontend_configs=("frontend-namespace.yaml" "frontend-deployment.yaml" "frontend-service.yaml" "frontend-ingress.yaml")

for config in "${frontend_configs[@]}"; do
  apply_config "/home/sellinios/aethra/microk8s/$config"
done

# Apply Kubernetes configurations for backend
log "Applying Kubernetes configurations for backend..."
backend_configs=("backend-namespace.yaml" "backend-deployment.yaml" "backend-service.yaml" "postgres-deployment.yaml")

for config in "${backend_configs[@]}"; do
  apply_config "/home/sellinios/aethra/microk8s/$config"
done

# Apply Kubernetes configurations for ingress
log "Applying Kubernetes configurations for ingress..."
ingress_configs=("nginx-ingress-service.yaml" "cluster-issuer.yaml" "tls-certificate.yaml")

for config in "${ingress_configs[@]}"; do
  apply_config "/home/sellinios/aethra/microk8s/$config"
done

# Wait for all pods to be running
wait_for_pods $FRONTEND_NAMESPACE 300
wait_for_pods $BACKEND_NAMESPACE 300
wait_for_pods $INGRESS_NAMESPACE 300

# Verify deployment
log "Verifying frontend deployment..."
microk8s kubectl get pods -n $FRONTEND_NAMESPACE
microk8s kubectl get svc -n $FRONTEND_NAMESPACE
microk8s kubectl get ingress -n $FRONTEND_NAMESPACE

log "Verifying backend deployment..."
microk8s kubectl get pods -n $BACKEND_NAMESPACE
microk8s kubectl get svc -n $BACKEND_NAMESPACE

log "Verifying nginx ingress service deployment..."
microk8s kubectl get svc -n $INGRESS_NAMESPACE

# Verify Ingress IP and status
log "Checking Ingress status..."
INGRESS_IP=$(microk8s kubectl get ingress frontend-ingress -n $FRONTEND_NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
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
