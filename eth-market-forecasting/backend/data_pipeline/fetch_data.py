import os
import requests
import json
import sqlite3
import pandas as pd
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DUNE_API_KEY = os.getenv("DUNE_API_KEY")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Database path
DB_PATH = "backend/data_pipeline/market_data.db"
JSON_PATH = "backend/data_pipeline/market_share_data.json"


### 📌 1️⃣ Fetch Market Share Data from Dune API
def fetch_market_share(market="dex", chain="ethereum"):
    """
    Fetches DEX or NFT market share data from Dune API.
    
    :param market: "dex" for DEXs or "nft" for NFT marketplaces.
    :param chain: Blockchain name (e.g., ethereum, polygon, bnb).
    :return: JSON response with market share data or None if the request fails.
    """
    url = f"https://api.dune.com/api/v1/marketshare/{market}/{chain}"
    headers = {"X-Dune-Api-Key": DUNE_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Dune API request failed: {e}")
        return None


### 📌 2️⃣ Fetch ETH Price from CoinGecko
def fetch_eth_price():
    """
    Fetches the latest Ethereum price from CoinGecko.
    :return: ETH price in USD or None if the request fails.
    """
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("ethereum", {}).get("usd")
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ CoinGecko API request failed: {e}")
        return None


### 📌 3️⃣ Fetch Ethereum Gas Price from Etherscan
def fetch_gas_price():
    """
    Fetches the latest Ethereum gas price from Etherscan.
    :return: Gas price data as a dictionary or None if the request fails.
    """
    url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "1":
            return {
                "low": data["result"]["SafeGasPrice"],
                "average": data["result"]["ProposeGasPrice"],
                "high": data["result"]["FastGasPrice"]
            }
        else:
            logging.warning(f"⚠ Etherscan API returned an error: {data}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Etherscan API request failed: {e}")
        return None


### 📌 4️⃣ Save Data to JSON File
def save_to_json(data, file_path=JSON_PATH):
    """
    Saves market data to a JSON file.
    
    :param data: Data to save.
    :param file_path: Path to the JSON file.
    """
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        logging.info(f"✅ Market share data saved to {file_path}")
    except IOError as e:
        logging.error(f"❌ Failed to save JSON data: {e}")


### 📌 5️⃣ Store Data in SQLite Database
def store_market_data(market_data, gas_price):
    """
    Stores market share, ETH price, and gas price data in an SQLite database.

    :param market_data: Market share data fetched from Dune API.
    :param gas_price: Gas price data fetched from Etherscan API.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_share (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            market TEXT,
            blockchain TEXT,
            project TEXT,
            version TEXT,
            volume_usd REAL,
            trades INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eth_price (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            price REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gas_price (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            low REAL,
            average REAL,
            high REAL
        )
    """)

    # Insert ETH price data
    eth_price = fetch_eth_price()
    if eth_price:
        cursor.execute("INSERT INTO eth_price (timestamp, price) VALUES (?, ?)", 
                       (datetime.now(), eth_price))
        logging.info("✅ ETH price data stored successfully.")
    else:
        logging.warning("⚠ ETH price data could not be retrieved.")

    # Insert Gas Price Data
    if gas_price:
        cursor.execute("INSERT INTO gas_price (timestamp, low, average, high) VALUES (?, ?, ?, ?)", 
                       (datetime.now(), gas_price["low"], gas_price["average"], gas_price["high"]))
        logging.info("✅ Gas price data stored successfully.")
    else:
        logging.warning("⚠ Gas price data could not be retrieved.")

    # Insert market share data
    if "result" in market_data and "rows" in market_data["result"]:
        rows = market_data["result"]["rows"]
        batch_data = [
            (
                datetime.now(),
                row.get("market"),
                row.get("blockchain"),
                row.get("project"),
                row.get("version"),
                row.get("volume_usd"),
                row.get("trades")
            )
            for row in rows
        ]

        cursor.executemany("""
            INSERT INTO market_share (timestamp, market, blockchain, project, version, volume_usd, trades)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, batch_data)

        logging.info(f"✅ Stored {len(batch_data)} market share records.")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    logging.info("🚀 Fetching market share data...")
    market_data = fetch_market_share()

    logging.info("⛽ Fetching Ethereum gas price data...")
    gas_price_data = fetch_gas_price()

    if market_data:
        save_to_json(market_data)
        store_market_data(market_data, gas_price_data)
    else:
        logging.error("❌ Failed to fetch market share data.")
