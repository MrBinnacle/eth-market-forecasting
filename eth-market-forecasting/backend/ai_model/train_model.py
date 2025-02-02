import os
import sqlite3
import numpy as np
import pandas as pd
import xgboost as xgb
import lightgbm as lgb
import joblib
import logging
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Database Path
DB_PATH = "backend/data_pipeline/market_data.db"
MODEL_PATH = "backend/ai_model/eth_forecast_model.pkl"

### 📌 1️⃣ Load Data from SQLite Database
def load_data():
    """
    Loads ETH market data along with market share and gas price data.
    Returns a preprocessed DataFrame ready for training.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        
        # Load ETH Price Data
        eth_price = pd.read_sql_query("SELECT * FROM eth_price", conn)
        
        # Load Market Share Data
        market_share = pd.read_sql_query("SELECT * FROM market_share", conn)
        
        # Load Gas Price Data
        gas_price = pd.read_sql_query("SELECT * FROM gas_price", conn)

        conn.close()

        # Convert timestamps to datetime
        eth_price["timestamp"] = pd.to_datetime(eth_price["timestamp"])
        market_share["timestamp"] = pd.to_datetime(market_share["timestamp"])
        gas_price["timestamp"] = pd.to_datetime(gas_price["timestamp"])

        # Merge datasets on timestamp
        merged_data = eth_price.merge(market_share, on="timestamp", how="left").merge(gas_price, on="timestamp", how="left")

        # Drop unused columns
        merged_data.drop(columns=["id_x", "id_y", "id"], errors="ignore", inplace=True)

        logging.info(f"✅ Loaded dataset with {len(merged_data)} rows.")
        return merged_data

    except sqlite3.Error as e:
        logging.error(f"❌ Database error: {e}")
        return None


### 📌 2️⃣ Preprocess Data for Training
def preprocess_data(df):
    """
    Prepares data for training.
    - Handles missing values
    - Splits into training & testing sets
    """
    df.fillna(method="ffill", inplace=True)  # Forward fill missing values
    df["timestamp"] = df["timestamp"].astype("int64") // 10**9  # Convert to Unix timestamp

    X = df.drop(columns=["price"])  # Features
    y = df["price"]  # Target (ETH Price)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    logging.info(f"✅ Data split into {len(X_train)} training and {len(X_test)} test samples.")
    return X_train, X_test, y_train, y_test


### 📌 3️⃣ Train & Save Model
def train_and_save_model(X_train, y_train):
    """
    Trains an XGBoost model and saves it for future predictions.
    """
    model = xgb.XGBRegressor(
        n_estimators=200, 
        learning_rate=0.05, 
        max_depth=5, 
        objective="reg:squarederror"
    )
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)
    logging.info(f"✅ Model trained and saved at {MODEL_PATH}")
    return model


### 📌 4️⃣ Evaluate Model
def evaluate_model(model, X_test, y_test):
    """
    Evaluates the trained model on test data.
    """
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    logging.info(f"📊 Model Evaluation:")
    logging.info(f"🔹 MAE: {mae:.4f}")
    logging.info(f"🔹 MSE: {mse:.4f}")
    logging.info(f"🔹 RMSE: {rmse:.4f}")

    return mae, mse, rmse


if __name__ == "__main__":
    logging.info("🚀 Starting ETH Market Forecast Model Training...")

    # Load and preprocess data
    data = load_data()
    if data is not None:
        X_train, X_test, y_train, y_test = preprocess_data(data)

        # Train model
        model = train_and_save_model(X_train, y_train)

        # Evaluate model
        evaluate_model(model, X_test, y_test)
    else:
        logging.error("❌ No data available for training.")
