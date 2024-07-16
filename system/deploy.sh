#!/bin/bash

# Apply Kubernetes configurations for frontend
echo "Applying Kubernetes configurations for frontend..."
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/frontend-namespace.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/frontend-deployment.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/frontend-service.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/frontend-ingress.yaml

if [ $? -ne 0 ]; then
  echo "Failed to apply frontend Kubernetes configurations. Exiting."
  exit 1
fi

# Apply Kubernetes configurations for backend
echo "Applying Kubernetes configurations for backend..."
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/backend-namespace.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/backend-deployment.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/backend-service.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/postgres-deployment.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/database-secret.yaml

if [ $? -ne 0 ]; then
  echo "Failed to apply backend Kubernetes configurations. Exiting."
  exit 1
fi

# Apply Kubernetes configurations for ingress
echo "Applying Kubernetes configurations for ingress..."
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/ingress-namespace.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/nginx-ingress-service.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/cluster-issuer.yaml
microk8s kubectl apply -f /home/sellinios/aethra/microk8s/tls-certificate.yaml

if [ $? -ne 0 ]; then
  echo "Failed to apply ingress Kubernetes configurations. Exiting."
  exit 1
fi

echo "All Kubernetes configurations applied successfully."
