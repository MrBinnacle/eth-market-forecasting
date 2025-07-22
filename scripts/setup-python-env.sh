#!/bin/bash

echo "🔧 Setting up Python virtual environment..."

if [ -d ".venv" ]; then
  echo "✅ Virtual environment already exists at .venv/"
else
  echo "📦 Creating new virtual environment..."
  python -m venv .venv || { echo "❌ Python venv creation failed."; exit 1; }
fi

echo "⚙️ Activating virtual environment..."
source .venv/bin/activate

if [ -f "backend/requirements.txt" ]; then
  echo "📦 Installing Python dependencies from backend/requirements.txt..."
  pip install -r backend/requirements.txt
else
  echo "⚠️ No requirements.txt found. Installing pytest manually..."
  pip install pytest
fi

echo "✅ Python environment setup complete."
