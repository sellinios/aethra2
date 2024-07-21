#!/bin/bash

# Ensure the script is run with superuser privileges if necessary
if [ "$EUID" -ne 0 ]; then
  echo "Some operations require root privileges. Please run as root or with sudo."
  exit 1
fi

# Log file location
LOGFILE="/var/log/docker_cleanup.log"
echo "Starting cleanup at $(date)" >> $LOGFILE

# Cleanup Kubernetes ReplicaSets
echo "Cleaning up old Kubernetes ReplicaSets..." | tee -a $LOGFILE
# Delete old ReplicaSets in frontend namespace
microk8s kubectl get rs -n frontend | awk '/frontend/ && $2 == "0" {print $1}' | xargs -r microk8s kubectl delete rs -n frontend
# Delete old ReplicaSets in backend namespace
microk8s kubectl get rs -n backend | awk '/backend/ && $2 == "0" {print $1}' | xargs -r microk8s kubectl delete rs -n backend

# Stop and remove all containers
echo "Stopping all running containers..." | tee -a $LOGFILE
CONTAINER_IDS=$(docker ps -aq)
if [ -n "$CONTAINER_IDS" ]; then
  docker stop $CONTAINER_IDS
  echo "Removing all containers..." | tee -a $LOGFILE
  docker rm $CONTAINER_IDS
else
  echo "No containers to stop and remove." | tee -a $LOGFILE
fi

# Remove all images except critical ones
echo "Removing Docker images except critical ones..." | tee -a $LOGFILE
CRITICAL_IMAGES="sellinios/backend:20240721111758"
IMAGE_IDS=$(docker images -q | grep -vE "$(echo $CRITICAL_IMAGES | sed 's/ /|/g')")
if [ -n "$IMAGE_IDS" ]; then
  docker rmi -f $IMAGE_IDS
else
  echo "No images to remove." | tee -a $LOGFILE
fi

# Optional: Remove unused volumes and networks
echo "Removing unused volumes and networks..." | tee -a $LOGFILE
docker volume prune -f | tee -a $LOGFILE
docker network prune -f | tee -a $LOGFILE

# Clean up build cache (optional)
echo "Removing build cache..." | tee -a $LOGFILE
docker builder prune -f | tee -a $LOGFILE

echo "Cleanup complete at $(date)" | tee -a $LOGFILE
