# ETH Market Forecasting Dashboard

[![CI](https://github.com/MrBinnacle/eth-market-forecasting/actions/workflows/ci.yml/badge.svg)](https://github.com/MrBinnacle/eth-market-forecasting/actions/workflows/ci.yml)
[![Snyk](https://snyk.io/test/github/MrBinnacle/eth-market-forecasting/badge.svg)](https://snyk.io/test/github/MrBinnacle/eth-market-forecasting)

This repository contains a small end‑to‑end system for forecasting the price of
Ethereum.  Market data is fetched and stored in SQLite, a machine‐learning model
is trained, and a simple dashboard displays predictions.  The React dashboard is
served with Vite while the Python backend exposes a Dash/Flask interface.

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
npm install
npm run dev
```

### Environment Variables

```
DUNE_API_KEY=<your-dune-key>
ETHERSCAN_API_KEY=<your-etherscan-key>
DEBUG=false
DASHBOARD_UPDATE_INTERVAL=60000
API_TIMEOUT=10
```

## 🧪 Running Tests

- **Python**

  ```bash
  pytest -q
  ```

- **Frontend** (Vitest)

  ```bash
  npm run test
  ```

- **Security Scan** (Snyk)

  ```bash
  npx snyk test
  ```

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
npm install
```

#### 3. Run Tests

* Python:

  ```bash
  pytest -q
  ```

* JavaScript:

  ```bash
  npm run test
  ```

#### 4. Security Scan (via Snyk)

```bash
npx snyk test
```

