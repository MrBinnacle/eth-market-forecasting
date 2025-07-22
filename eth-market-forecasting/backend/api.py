from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import joblib
import numpy as np
import sqlite3
import logging
import pandas as pd

# Load environment variables
load_dotenv()
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define paths
MODEL_PATH = "backend/ai_model/eth_forecast_model.pkl"
DB_PATH = "backend/data_pipeline/market_data.db"

# Initialize Flask app with CORS enabled
app = Flask(__name__)
CORS(app)

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
    except Exception as e:
        logging.error(f"❌ Error loading model: {e}")
    return None

# Load model once at startup
model = load_model()

def fetch_latest_data():
    """
    Fetches the latest ETH price, market share, and gas price data from the database.
    Returns a dictionary with the required features or None if any data is missing.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Fetch the most recent ETH price
            eth_query = "SELECT price FROM eth_price ORDER BY timestamp DESC LIMIT 1"
            eth_price_df = pd.read_sql_query(eth_query, conn)
            
            # Fetch the most recent market share data
            market_query = "SELECT volume_usd FROM market_share ORDER BY timestamp DESC LIMIT 1"
            market_share_df = pd.read_sql_query(market_query, conn)
            
            # Fetch the most recent gas price data
            gas_query = "SELECT average FROM gas_price ORDER BY timestamp DESC LIMIT 1"
            gas_price_df = pd.read_sql_query(gas_query, conn)

        if eth_price_df.empty or market_share_df.empty or gas_price_df.empty:
            logging.warning("⚠ Missing data for prediction.")
            return None

        return {
            "eth_price": eth_price_df["price"].iloc[0],
            "market_volume": market_share_df["volume_usd"].iloc[0],
            "gas_price": gas_price_df["average"].iloc[0]
        }
    except sqlite3.Error as e:
        logging.error(f"❌ Database error: {e}")
    except Exception as e:
        logging.error(f"❌ Unexpected error fetching data: {e}")
    return None

@app.route('/api/predict', methods=['GET'])
def predict_eth_price():
    """
    API endpoint to predict ETH price using the trained model and the latest market data.
    """
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    latest_data = fetch_latest_data()
    if latest_data is None:
        return jsonify({"error": "No valid input data available"}), 500

    try:
        features = np.array([[latest_data["eth_price"], latest_data["market_volume"], latest_data["gas_price"]]])
        predicted_price = model.predict(features)[0]
    except Exception as e:
        logging.error(f"❌ Prediction error: {e}")
        return jsonify({"error": "Prediction failed"}), 500

    return jsonify({"predicted_price": float(predicted_price)})

@app.route('/api/market-data', methods=['GET'])
def get_latest_market_data():
    """
    API endpoint to fetch the latest ETH price, market share, and gas price.
    """
    latest_data = fetch_latest_data()
    if latest_data is None:
        return jsonify({"error": "Missing market data"}), 500

    return jsonify(latest_data)

if __name__ == '__main__':
    logging.info("🚀 Starting AI-Powered Ethereum Price Prediction API...")
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
