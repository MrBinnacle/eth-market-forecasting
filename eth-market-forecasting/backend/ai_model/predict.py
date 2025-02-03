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

MODEL = load_model()

def fetch_latest_data():
    """
    Fetches the latest available market data from SQLite database.
    Uses the closest timestamp match if an exact one isn't available.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
                SELECT e.timestamp, 
                       COALESCE(m.volume_usd, 0) AS volume_usd, 
                       COALESCE(g.average, 0) AS gas_price
                FROM eth_price e
                LEFT JOIN market_share m ON m.timestamp = (
                    SELECT timestamp FROM market_share 
                    WHERE timestamp <= e.timestamp 
                    ORDER BY timestamp DESC LIMIT 1
                )
                LEFT JOIN gas_price g ON g.timestamp = (
                    SELECT timestamp FROM gas_price 
                    WHERE timestamp <= e.timestamp 
                    ORDER BY timestamp DESC LIMIT 1
                )
                ORDER BY e.timestamp DESC LIMIT 1;
            """
            df = pd.read_sql(query, conn)

        if df.empty:
            logging.warning("⚠ Missing data for prediction.")
            return None

        # Convert timestamp to Unix format
        df["timestamp"] = pd.to_datetime(df["timestamp"]).astype("int64") // 10**9
        logging.info(f"✅ Latest feature data retrieved successfully: {df}")
        return df.values

    except sqlite3.Error as e:
        logging.error(f"❌ Database error: {e}")
    return None


def predict_eth_price():
    if MODEL is None:
        return None

    latest_features = fetch_latest_data()
    if latest_features is None:
        return None

    try:
        feature_names = ["timestamp", "volume_usd", "gas_price"]
        prediction = MODEL.predict(pd.DataFrame(latest_features, columns=feature_names))
        return float(prediction[0])
    except Exception as e:
        logging.error(f"❌ Error during prediction: {e}")
    return None

if __name__ == "__main__":
    logging.info("🚀 Running ETH Price Prediction...")
    predicted_price = predict_eth_price()
    print(f"📈 Predicted ETH Price: ${predicted_price:.2f}" if predicted_price else "❌ Failed to generate prediction.")
