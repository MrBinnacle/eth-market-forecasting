#!/bin/bash
set -e

# Verify Node.js installation
if ! command -v node >/dev/null 2>&1; then
  echo "❌ Node.js is not installed" >&2
  exit 1
fi

# Attempt dependency install only if node_modules missing
if [ ! -d frontend/node_modules ]; then
  echo "Installing Node dependencies..."
  npm install --prefix frontend || echo "⚠️ npm install failed - offline?"
fi

# Check presence of common CLI tools without installing
for cmd in vite vitest snyk; do
  if ! npx --prefix frontend --no-install "$cmd" --version >/dev/null 2>&1; then
    echo "⚠️ $cmd not available"
  fi
done
