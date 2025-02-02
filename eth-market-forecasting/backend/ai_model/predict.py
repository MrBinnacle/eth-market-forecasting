import os
import joblib
import numpy as np
import sqlite3
import logging
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Paths
MODEL_PATH = "backend/ai_model/eth_forecast_model.pkl"
DB_PATH = "backend/data_pipeline/market_data.db"

# Load the trained model
def load_model():
    """
    Loads the trained machine learning model for ETH price forecasting.
    """
    try:
        model = joblib.load(MODEL_PATH)
        logging.info("✅ Model loaded successfully.")
        return model
    except FileNotFoundError:
        logging.error(f"❌ Model file not found at {MODEL_PATH}")
        return None

# Fetch latest real-time features from SQLite
def fetch_latest_data():
    """
    Fetches the latest available market share, ETH price, and gas price data from the database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)

        # Load the most recent ETH price
        eth_price = pd.read_sql_query("SELECT * FROM eth_price ORDER BY timestamp DESC LIMIT 1", conn)

        # Load the most recent market share data
        market_share = pd.read_sql_query("SELECT * FROM market_share ORDER BY timestamp DESC LIMIT 1", conn)

        # Load the most recent gas price data
        gas_price = pd.read_sql_query("SELECT * FROM gas_price ORDER BY timestamp DESC LIMIT 1", conn)

        conn.close()

        if eth_price.empty or market_share.empty or gas_price.empty:
            logging.warning("⚠ Missing data for prediction.")
            return None

        # Extract relevant values
        latest_eth_price = eth_price["price"].values[0]
        latest_market_volume = market_share["volume_usd"].values[0]
        latest_gas_price = gas_price["average"].values[0]

        return np.array([[latest_eth_price, latest_market_volume, latest_gas_price]])

    except sqlite3.Error as e:
        logging.error(f"❌ Database error: {e}")
        return None

# Predict ETH price using real-time features
def predict_eth_price():
    """
    Predicts ETH price using the trained model and latest market data.
    """
    model = load_model()
    if model is None:
        logging.error("❌ Prediction failed: No model loaded.")
        return None

    latest_features = fetch_latest_data()
    if latest_features is None:
        logging.error("❌ Prediction failed: No valid input data.")
        return None

    prediction = model.predict(latest_features)
    return prediction[0]

if __name__ == "__main__":
    logging.info("🚀 Running ETH Price Prediction...")
    predicted_price = predict_eth_price()

    if predicted_price is not None:
        print(f"📈 Predicted ETH Price: ${predicted_price:.2f}")
    else:
        print("❌ Failed to generate prediction.")
