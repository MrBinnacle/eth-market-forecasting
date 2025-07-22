
from backend.ai_model.model_utils import load_model, fetch_latest_data

MODEL = load_model()


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
    if predicted_price is not None:
        print(f"📈 Predicted ETH Price: ${predicted_price:.2f}")
    else:
        print("❌ Failed to generate prediction.")
