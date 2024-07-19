#!/bin/bash

# Use microk8s kubectl
MICROK8S_KUBECTL="microk8s kubectl"

# Find a running pod with the label app=backend in the backend namespace
POD_NAME=$($MICROK8S_KUBECTL get pods -n backend -l app=backend -o jsonpath="{.items[0].metadata.name}")

if [ -z "$POD_NAME" ]; then
  echo "No running backend pod found."
  exit 1
fi

echo "Found backend pod: $POD_NAME"

# Set up port forwarding
$MICROK8S_KUBECTL port-forward pod/$POD_NAME 8000:8000 -n backend
