import sqlite3
import pandas as pd
import numpy as np
import logging
import os
import joblib
from datetime import datetime
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Database and model paths
DB_PATH = "backend/data_pipeline/market_data.db"
MODEL_PATH = "backend/ai_model/eth_forecast_model.pkl"

def load_data():
    """
    Loads market data from SQLite database.
    
    Returns:
        DataFrame: Pandas DataFrame with relevant features.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
    SELECT e.timestamp, e.price, 
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
    ORDER BY e.timestamp ASC;
"""
            df = pd.read_sql(query, conn)

        if df.empty:
            logging.error("❌ Loaded dataset is empty.")
            return None

        logging.info(f"✅ Loaded dataset with {len(df)} rows.")
        return df

    except sqlite3.Error as e:
        logging.error(f"❌ Database error while loading data: {e}")
        return None
    except Exception as e:
        logging.error(f"❌ Unexpected error while loading data: {e}")
        return None

def preprocess_data(df):
    """
    Prepares data for training:
    - Handles missing values with forward fill.
    - Converts timestamp to Unix format.
    - Splits the data into training and testing sets.

    Args:
        df (DataFrame): Merged DataFrame with market data.

    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    if df is None or df.empty:
        logging.error("❌ DataFrame is empty or None.")
        return None, None, None, None

    # Forward fill missing values and fix data type warnings
    df.ffill(inplace=True)
    df = df.infer_objects(copy=False)

    # Convert timestamp to Unix timestamp (seconds)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["timestamp"] = df["timestamp"].astype("int64") // 10**9

    # Ensure "price" column exists
    if "price" not in df.columns:
        logging.error("❌ 'price' column is missing from the dataset.")
        return None, None, None, None

    # Define features and target variable
    X = df[["timestamp", "volume_usd", "gas_price"]]  # Train on all three features
    y = df["price"]

    # Split data preserving time order (no shuffling)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    logging.info(f"✅ Data split into {len(X_train)} training and {len(X_test)} test samples.")

    return X_train, X_test, y_train, y_test

def train_and_evaluate(X_train, X_test, y_train, y_test):
    """
    Trains a machine learning model and evaluates it.

    Args:
        X_train, X_test, y_train, y_test: Training and testing datasets.

    Returns:
        model: Trained model.
    """
    if any(v is None for v in [X_train, X_test, y_train, y_test]):
        logging.error("❌ Training aborted due to missing data.")
        return None

    # Initialize and train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate model performance
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    logging.info(f"✅ Model trained and saved at {MODEL_PATH}")
    logging.info(f"📊 Model Evaluation Metrics:")
    logging.info(f"🔹 MAE: {mae:.4f}")
    logging.info(f"🔹 MSE: {mse:.4f}")
    logging.info(f"🔹 RMSE: {rmse:.4f}")

    return model

def save_model(model):
    """
    Saves the trained model to a file.

    Args:
        model: Trained machine learning model.
    """
    if model:
        joblib.dump(model, MODEL_PATH)
        logging.info(f"✅ Model successfully saved to {MODEL_PATH}")
    else:
        logging.error("❌ No model to save.")

if __name__ == "__main__":
    logging.info("🚀 Starting ETH Market Forecast Model Training...")

    # Load and preprocess data
    data = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(data)

    # Train and evaluate the model
    model = train_and_evaluate(X_train, X_test, y_train, y_test)

    # Save the model if training was successful
    save_model(model)
