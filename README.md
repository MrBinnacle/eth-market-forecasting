# ETH Market Forecasting Dashboard

[![CI](https://github.com/MrBinnacle/eth-market-forecasting/actions/workflows/ci.yml/badge.svg)](https://github.com/MrBinnacle/eth-market-forecasting/actions/workflows/ci.yml)
[![Snyk](https://snyk.io/test/github/MrBinnacle/eth-market-forecasting/badge.svg)](https://snyk.io/test/github/MrBinnacle/eth-market-forecasting)

This repository contains a small end‑to‑end system for forecasting the price of
Ethereum. Market data is fetched and stored in SQLite, a machine‑learning model
is trained, and a simple dashboard displays predictions. The React dashboard is
served with Vite while the Python backend exposes a Dash/Flask API and
dashboard.

🔗 **Live Site**: <https://MrBinnacle.github.io/eth-market-forecasting>

## 📦 Tech Stack

- **React + Vite** – UI served on GitHub Pages
- **Python** – Flask, Dash and scikit‑learn
- **SQLite** – lightweight storage for fetched market data

## 🧠 Features

- Dashboard visualization for ETH and example portfolio data
- Emergency‑fund alert and learning plan template
- ML pipeline using a Random Forest model for ETH price forecasting

## 🚀 Getting Started

1. Copy `.env.example` to `.env` and add API keys for Dune and Etherscan.
2. Install dependencies and run the full pipeline:

   ```bash
   chmod +x run.sh
   ./run.sh
   ```

   The script installs Python requirements, fetches market data, trains the
   model and launches the dashboard.

To develop the React frontend separately:

```bash
npm install --prefix frontend
npm start --prefix frontend
```

### Project Structure

```
backend/   # Python API, data pipeline and Dash app
frontend/  # React dashboard served with Vite
tests/     # Pytest and Vitest examples
```

### Architecture

1. **Data Pipeline** – Python scripts under `backend/data_pipeline` fetch market
   data from Dune, Etherscan and DeFiLlama and store it in SQLite.
2. **AI Model** – `backend/ai_model` trains a Random Forest model from the
   stored data and exposes predictions through `backend/api.py`.
3. **Dash Dashboard** – `backend/dashboard/app.py` displays predictions.
4. **React Frontend** – `frontend` contains a simple React interface built with
   Vite and hosted on GitHub Pages.

### Environment Variables

The project expects a `.env` file in the repository root. The following
variables are used:

```
DUNE_API_KEY=<your-dune-key>        # access to Dune Analytics API
ETHERSCAN_API_KEY=<your-etherscan-key>  # required for gas price queries
DEBUG=false                        # enable verbose Flask logging
DASHBOARD_UPDATE_INTERVAL=60000    # dashboard refresh interval in ms
API_TIMEOUT=10                     # HTTP client timeout in seconds
```

**Never commit real API keys**. Use `.env.example` as a template and keep your
`.env` file private.

### API Endpoints

The Flask API exposes two simple endpoints once the server is running:

- `GET /api/predict` – returns the latest predicted ETH price using the
  trained model.
- `GET /api/market-data` – returns the most recent market data stored in the
  SQLite database.

## 🧪 Running Tests

- **Python**

  ```bash
  pytest -q
  ```

- **Frontend** (Vitest)

  ```bash
  npm run test --prefix frontend
  ```

- **Security Scan** (Snyk)

  ```bash
  npx snyk test
  ```
  CI also runs this scan on every pull request.

## Local Setup

### Prerequisites

- [Node.js](https://nodejs.org/) >= v18
- [Python 3.7+](https://www.python.org/)
- [npm](https://www.npmjs.com/)
- (Optional) [Vitest VS Code extension](https://marketplace.visualstudio.com/items?itemName=ZixuanChen.vitest-explorer)

---

### Setup

#### 1. Python Environment

```bash
source scripts/setup-python-env.sh
```

#### 2. Node + Project Dependencies

```bash
npm install --prefix frontend
```

#### 3. Run Tests

* Python:

  ```bash
  pytest -q
  ```

* JavaScript:

  ```bash
  npm run test --prefix frontend
  ```

#### 4. Security Scan (via Snyk)

```bash
npx snyk test
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
For bug reports include steps to reproduce and any relevant logs.

