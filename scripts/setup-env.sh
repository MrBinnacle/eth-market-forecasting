#!/bin/bash
# Optional: make this executable with chmod +x scripts/setup-env.sh

echo "Setting up environment..."
npm ci
pip install -r backend/requirements.txt

