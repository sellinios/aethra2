#!/bin/bash

# Pull the latest code from the repository
cd /home/sellinios/aethra || { echo "Directory /home/sellinios/aethra not found. Exiting."; exit 1; }

# Check the branch name
BRANCH_NAME="master" # Updated to use "master" branch

# Pull the latest code
git pull origin $BRANCH_NAME

# Run the build script
/home/sellinios/aethra/system/build.sh

# Run the deploy script
/home/sellinios/aethra/system/deploy.sh
