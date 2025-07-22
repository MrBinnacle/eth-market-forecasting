
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
import numpy as np
from backend.ai_model.model_utils import load_model, fetch_latest_data

# Load environment variables
load_dotenv()
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Flask app with CORS enabled
app = Flask(__name__)
CORS(app)

# Load model once at startup
model = load_model()


@app.route('/api/predict', methods=['GET'])
def predict_eth_price():
    """
    API endpoint to predict ETH price using the trained model and the latest market data.
    """
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    latest_features = fetch_latest_data()
    if latest_features is None:
        return jsonify({"error": "No valid input data available"}), 500

    try:
        predicted_price = model.predict(latest_features)[0]
    except Exception as e:
        logging.error(f"❌ Prediction error: {e}")
        return jsonify({"error": "Prediction failed"}), 500

    return jsonify({"predicted_price": float(predicted_price)})


@app.route('/api/market-data', methods=['GET'])
def get_latest_market_data():
    """
    API endpoint to fetch the latest ETH price, market share, and gas price.
    """
    latest_features = fetch_latest_data()
    if latest_features is None:
        return jsonify({"error": "Missing market data"}), 500

    # Convert features array to a dict for response
    # Assuming columns: timestamp, volume_usd, gas_price
    feature_names = ["timestamp", "volume_usd", "gas_price"]
    data_dict = dict(zip(feature_names, latest_features[0]))
    return jsonify(data_dict)

if __name__ == '__main__':
    logging.info("🚀 Starting AI-Powered Ethereum Price Prediction API...")
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)
