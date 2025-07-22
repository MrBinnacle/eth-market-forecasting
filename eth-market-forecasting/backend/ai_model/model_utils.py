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

MODEL_PATH = "backend/ai_model/eth_forecast_model.pkl"
DB_PATH = "backend/data_pipeline/market_data.db"

def load_model(model_path=MODEL_PATH):
    """
    Loads the trained machine learning model for ETH price forecasting.
    """
    try:
        model = joblib.load(model_path)
        logging.info("✅ Model loaded successfully.")
        return model
    except FileNotFoundError:
        logging.error(f"❌ Model file not found at {model_path}")
    except Exception as e:
        logging.error(f"❌ Error loading model: {e}")
    return None

def fetch_latest_data(db_path=DB_PATH):
    """
    Fetches the latest available market data from SQLite database.
    Uses the closest timestamp match if an exact one isn't available.
    """
    try:
        with sqlite3.connect(db_path) as conn:
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
