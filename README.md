# ETH Market Forecasting Dashboard

This project provides a simple dashboard and backend pipeline for predicting the price of Ethereum. The frontend is a React application served with Vite while the backend collects market data, trains a model and exposes a small Flask API.

🔗 **Live Site**: <https://MrBinnacle.github.io/eth-market-forecasting>

## 📦 Tech Stack
- React + Vite
- Python (Flask, Dash, scikit‑learn)
- GitHub Pages Deployment

## 🧠 Features
- Dashboard visualization for ETH and crypto positions
- Emergency fund alert and learning plan system
- Decision framework for action planning
- Example machine learning pipeline for ETH price forecasting

## 🚀 Getting Started
1. Copy `.env.example` to `.env` and fill in your API keys.
2. Install Node and Python dependencies and run the full pipeline:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
   The script installs Python requirements, fetches data, trains the model and launches the dashboard.

The frontend alone can be run in development mode with:
```bash
npm install
npm run dev
```

## 🧪 Run Tests
- Python tests
  ```bash
  pytest -q
  ```
- Frontend tests (Vitest)
  ```bash
  npm run test
  ```
