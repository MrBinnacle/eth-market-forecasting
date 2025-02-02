#!/bin/bash
# Ensure the script is executable: chmod +x run.sh

echo "Setting up environment..."
pip install -r backend/requirements.txt

echo "Starting data pipeline..."
# Run data fetching in the background; consider using a scheduler (e.g., cron) for production
python backend/data_pipeline/fetch_data.py &

echo "Training AI model..."
python backend/ai_model/train_model.py

echo "Launching dashboard..."
python frontend/dashboard.py
