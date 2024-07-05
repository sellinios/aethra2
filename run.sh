#!/bin/bash

echo "Select the script you want to run:"
echo "1) Docker Cleanup"
echo "2) Another script (add more options as needed)"

read -p "Enter the number of the script you want to run: " choice

case $choice in
  1)
    echo "Running Docker Cleanup..."
    ./system/docker_cleanup.sh
    ;;
  2)
    # Add the command for another script here
    echo "Another script option selected"
    ;;
  *)
    echo "Invalid choice"
    ;;
esac
