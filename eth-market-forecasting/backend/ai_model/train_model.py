import os
import sqlite3
import numpy as np
import pandas as pd
import xgboost as xgb
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

# Paths
DB_PATH = "backend/data_pipeline/market_data.db"
MODEL_PATH = "backend/ai_model/eth_forecast_model.pkl"


def load_data():
    """
    Loads ETH market data along with market share and gas price data from the SQLite database.
    Returns:
        DataFrame: A preprocessed DataFrame ready for training, or None on failure.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Load datasets from their respective tables
            eth_price = pd.read_sql_query("SELECT * FROM eth_price", conn)
            market_share = pd.read_sql_query("SELECT * FROM market_share", conn)
            gas_price = pd.read_sql_query("SELECT * FROM gas_price", conn)

        # Convert timestamps to datetime
        eth_price["timestamp"] = pd.to_datetime(eth_price["timestamp"])
        market_share["timestamp"] = pd.to_datetime(market_share["timestamp"])
        gas_price["timestamp"] = pd.to_datetime(gas_price["timestamp"])

        # Merge datasets on timestamp using left joins to preserve ETH price data
        merged_data = eth_price.merge(market_share, on="timestamp", how="left") \
                               .merge(gas_price, on="timestamp", how="left")

        # Drop any ambiguous or unused ID columns if present
        merged_data.drop(columns=["id", "id_x", "id_y"], errors="ignore", inplace=True)

        logging.info(f"✅ Loaded dataset with {len(merged_data)} rows.")
        return merged_data

    except sqlite3.Error as e:
        logging.error(f"❌ Database error while loading data: {e}")
    except Exception as e:
        logging.error(f"❌ Unexpected error while loading data: {e}")
    return None


def preprocess_data(df):
    """
    Prepares data for training:
      - Handles missing values with forward fill.
      - Converts timestamp to Unix seconds.
      - Splits the data into training and testing sets.
    
    Args:
        df (DataFrame): Merged DataFrame with market data.
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test) split from the data.
    """
    # Forward fill missing values
    df.fillna(method="ffill", inplace=True)

    # Convert timestamp to Unix timestamp (seconds)
    df["timestamp"] = df["timestamp"].astype("int64") // 10**9

    # Assume "price" is the target variable and drop it from features
    if "price" not in df.columns:
        logging.error("❌ 'price' column is missing from the dataset.")
        return None, None, None, None

    X = df.drop(columns=["price"])
    y = df["price"]

    # Split data preserving time order (no shuffling)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    logging.info(f"✅ Data split into {len(X_train)} training and {len(X_test)} test samples.")
    return X_train, X_test, y_train, y_test


def train_and_save_model(X_train, y_train):
    """
    Trains an XGBoost regressor on the provided training data and saves the model.
    
    Args:
        X_train (DataFrame): Training features.
        y_train (Series): Target variable.
    
    Returns:
        model: The trained XGBoost model.
    """
    try:
        model = xgb.XGBRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=5,
            objective="reg:squarederror",
            random_state=42
        )
        model.fit(X_train, y_train)
        joblib.dump(model, MODEL_PATH)
        logging.info(f"✅ Model trained and saved at {MODEL_PATH}")
        return model
    except Exception as e:
        logging.error(f"❌ Error during model training: {e}")
    return None


def evaluate_model(model, X_test, y_test):
    """
    Evaluates the trained model on test data and logs MAE, MSE, and RMSE.
    
    Args:
        model: The trained model.
        X_test (DataFrame): Test features.
        y_test (Series): Test target variable.
    
    Returns:
        tuple: (mae, mse, rmse)
    """
    try:
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
    
        logging.info("📊 Model Evaluation Metrics:")
        logging.info(f"🔹 MAE: {mae:.4f}")
        logging.info(f"🔹 MSE: {mse:.4f}")
        logging.info(f"🔹 RMSE: {rmse:.4f}")
        return mae, mse, rmse
    except Exception as e:
        logging.error(f"❌ Error during model evaluation: {e}")
    return None, None, None


if __name__ == "__main__":
    logging.info("🚀 Starting ETH Market Forecast Model Training...")

    # Load data from the database
    data = load_data()
    if data is None:
        logging.error("❌ No data available for training.")
        exit(1)

    # Preprocess data
    X_train, X_test, y_train, y_test = preprocess_data(data)
    if X_train is None:
        logging.error("❌ Preprocessing failed.")
        exit(1)

    # Train model and save
    model = train_and_save_model(X_train, y_train)
    if model is None:
        logging.error("❌ Model training failed.")
        exit(1)

    # Evaluate model performance
    evaluate_model(model, X_test, y_test)
