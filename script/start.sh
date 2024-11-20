#!/bin/bash

# Ensure Python is installed
if ! command -v python3 &> /dev/null; then
  echo "Python3 not found. Please install Python3 and try again."
  exit 1
fi

# Ensure pip is installed
if ! command -v pip &> /dev/null; then
  echo "pip not found. Installing pip..."
  python3 -m ensurepip --upgrade
fi

# Create and activate a virtual environment
if [ ! -d "venv" ]; then
  echo "Creating a virtual environment..."
  python3 -m venv venv
fi

echo "Activating the virtual environment..."
source venv/bin/activate

# Ensure dependencies are installed
if [ -f "requirements.txt" ]; then
  echo "Installing dependencies..."
  pip install --upgrade pip
  pip install -r requirements.txt
else
  echo "requirements.txt not found. Please ensure it exists with required packages."
  exit 1
fi

# Run the application from the app/ directory
if [ -f "app/main.py" ]; then
  echo "Running the PromocatoApp..."
  python app/main.py
else
  echo "Application file not found at app/main.py. Please ensure the file exists."
  exit 1
fi
