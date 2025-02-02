Write-Host "🚀 Starting Ethereum Market Forecasting System..."

# Activate virtual environment
& venv\Scripts\Activate

# Run data pipeline
Write-Host "📡 Fetching live ETH data..."
python backend/data_pipeline/fetch_data.py

# Train the model (only first-time or when retraining)
Write-Host "🤖 Training AI model..."
python backend/ai_model/train_model.py

# Start dashboard
Write-Host "📊 Launching dashboard at http://localhost:8050..."
python frontend/dashboard.py
