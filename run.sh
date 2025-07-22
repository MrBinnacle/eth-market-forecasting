#!/bin/bash
# Ensure the script is executable: chmod +x run.sh

echo "Setting up backend environment..."
if [ -f backend/requirements.txt ]; then
  pip install -r backend/requirements.txt
else
  echo "⚠️ requirements.txt not found" >&2
fi

echo "Starting data pipeline..."
# Run data fetching in the background; consider using a scheduler (e.g., cron) for production
python backend/data_pipeline/fetch_data.py &

echo "Training AI model..."
python backend/ai_model/train_model.py

echo "Launching dashboard..."
python backend/dashboard/app.py
