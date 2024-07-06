#!/bin/bash

echo "Select the script you want to run:"
echo "1) Docker Cleanup"
echo "2) Deploy microk8s"

read -p "Enter the number of the script you want to run: " choice

case $choice in
  1)
    echo "Running Docker Cleanup..."
    ./system/docker_cleanup.sh
    ;;
  2)
    echo "Deploy..."
    ./system/deploy.sh
    ;;
  *)
    echo "Invalid choice"
    ;;
esac
