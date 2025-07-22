#!/bin/bash
# Optional: make this executable with chmod +x scripts/setup-env.sh

set -e

echo "Setting up environment..."

# Prepare Node/JS environment
./scripts/bootstrap.sh || true

# Install Python dependencies if available
if [ -f backend/requirements.txt ]; then
  pip install -r backend/requirements.txt || echo "⚠️ pip install failed"
fi
