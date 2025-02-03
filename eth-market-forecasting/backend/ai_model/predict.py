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

def load_model():
    """
    Loads the trained machine learning model for ETH price forecasting.
    
    Returns:
        model: Trained model object if successful, else None.
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

# Cache the model at module level for efficiency.
MODEL = load_model()

def fetch_latest_data():
    """
    Fetches the latest available market data from the SQLite database.
    Specifically retrieves the most recent ETH price, market share volume, and gas price (average).
    
    Returns:
        np.ndarray: A 2D NumPy array with shape (1, 3) containing the features, or None if any data is missing.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Retrieve the most recent ETH price
            eth_price_df = pd.read_sql_query("SELECT price FROM eth_price ORDER BY timestamp DESC LIMIT 1", conn)
            # Retrieve the most recent market share data
            market_share_df = pd.read_sql_query("SELECT volume_usd FROM market_share ORDER BY timestamp DESC LIMIT 1", conn)
            # Retrieve the most recent gas price data
            gas_price_df = pd.read_sql_query("SELECT average FROM gas_price ORDER BY timestamp DESC LIMIT 1", conn)
        
        if eth_price_df.empty or market_share_df.empty or gas_price_df.empty:
            logging.warning("⚠ Missing data for prediction.")
            return None

        latest_eth_price = eth_price_df["price"].iloc[0]
        latest_market_volume = market_share_df["volume_usd"].iloc[0]
        latest_gas_price = gas_price_df["average"].iloc[0]

        logging.info("✅ Latest feature data retrieved successfully.")
        return np.array([[latest_eth_price, latest_market_volume, latest_gas_price]])

    except sqlite3.Error as e:
        logging.error(f"❌ Database error: {e}")
    except Exception as e:
        logging.error(f"❌ Unexpected error while fetching data: {e}")
    return None

def predict_eth_price():
    """
    Predicts the Ethereum (ETH) price using the trained model and the latest market data.
    
    Returns:
        float: The predicted ETH price, or None if prediction fails.
    """
    if MODEL is None:
        logging.error("❌ Prediction failed: Model is not loaded.")
        return None

    latest_features = fetch_latest_data()
    if latest_features is None:
        logging.error("❌ Prediction failed: Valid input data is missing.")
        return None

    try:
        prediction = MODEL.predict(latest_features)
        predicted_value = float(prediction[0])
        logging.info(f"✅ Prediction successful: ${predicted_value:.2f}")
        return predicted_value
    except Exception as e:
        logging.error(f"❌ Error during prediction: {e}")
    return None

if __name__ == "__main__":
    logging.info("🚀 Running ETH Price Prediction...")
    predicted_price = predict_eth_price()
    
    if predicted_price is not None:
        print(f"📈 Predicted ETH Price: ${predicted_price:.2f}")
    else:
        print("❌ Failed to generate prediction.")
