#!/bin/bash

# Ensure the script stops on errors
set -e

# Define colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Activating virtual environment for local development...${NC}"

# Activate the virtual environment
source venv/bin/activate

# Check if the virtual environment is activated by showing the Python version and executable
python_version=$(python --version)
python_executable=$(which python)

echo -e "${GREEN}Virtual environment activated.${NC}"
echo -e "Python version: ${GREEN}$python_version${NC}"
echo -e "Python executable: ${GREEN}$python_executable${NC}"

# Change to the backend directory
cd backend

# Provide instructions to the user
echo -e "${YELLOW}You are now in the virtual environment and inside the 'backend' directory. To run Django commands, use 'python manage.py <command>'.${NC}"
echo -e "${YELLOW}To deactivate the virtual environment, type 'deactivate'.${NC}"

# Keep the shell open and continue using the same session
$SHELL --rcfile <(echo "source ../venv/bin/activate")
