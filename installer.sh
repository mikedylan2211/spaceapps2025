#!/bin/bash
set -e

# Repo URL
REPO_URL="https://github.com/borystereschenko/Hackthon"
REPO_DIR="Hackthon"
MAIN_FILE="app.py"

# 1. Clone repo if not exists
if [ ! -d "$REPO_DIR" ]; then
    echo "Cloning repository..."
    git clone "$REPO_URL"
else
    echo "Updating repository..."
    cd "$REPO_DIR"
    git pull
    cd ..
fi

cd "$REPO_DIR"

# 2. Create venv if not exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# 3. Activate venv
source .venv/bin/activate

# 4. Install requirements (if exists)
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "No requirements.txt found. Skipping dependency installation."
fi

# 5. Run main file
if [ -f "$MAIN_FILE" ]; then
    echo "Running $MAIN_FILE..."
    streamlit run "$MAIN_FILE"
else
    echo "$MAIN_FILE not found!"
    exit 1
fi

