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

# Define paths
DB_PATH = "backend/data_pipeline/market_data.db"
JSON_PATH = "backend/data_pipeline/market_share_data.json"


def fetch_market_share(market="dex", chain="ethereum"):
    """
    Fetches DEX or NFT market share data from the Dune API.
    
    :param market: "dex" for DEXs or "nft" for NFT marketplaces.
    :param chain: Blockchain name (e.g., ethereum, polygon, bnb).
    :return: JSON response with market share data or None if the request fails.
    """
    url = f"https://api.dune.com/api/v1/marketshare/{market}/{chain}"
    headers = {"X-Dune-Api-Key": DUNE_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logging.info("✅ Market share data fetched successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Dune API request failed: {e}")
        return None


def fetch_gas_price():
    """
    Fetches the latest Ethereum gas price from the Etherscan API.
    
    :return: Dictionary containing gas price data or None if the request fails.
    """
    url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "1":
            logging.info("✅ Gas price data fetched successfully.")
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


def fetch_tvl():
    """
    Fetches the latest DeFi Total Value Locked (TVL) for Ethereum from the DeFiLlama API.
    
    :return: TVL in USD or None if the request fails.
    """
    url = "https://api.llama.fi/tvl/ethereum"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        tvl = data.get("tvl")
        if tvl is not None:
            logging.info("✅ TVL data fetched successfully.")
        else:
            logging.warning("⚠ TVL data missing in API response.")
        return tvl
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ DeFiLlama API request failed: {e}")
        return None


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


def create_tables(cursor):
    """
    Creates necessary tables in the SQLite database if they do not exist.
    
    :param cursor: SQLite cursor object.
    """
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS market_share (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            market TEXT,
            blockchain TEXT,
            project TEXT,
            version TEXT,
            volume_usd REAL,
            trades INTEGER
        );
        CREATE TABLE IF NOT EXISTS gas_price (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            low REAL,
            average REAL,
            high REAL
        );
        CREATE TABLE IF NOT EXISTS tvl (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            tvl REAL
        );
    """)


def store_market_data(market_data, gas_price, tvl):
    """
    Stores market share, TVL, and gas price data in an SQLite database.
    
    :param market_data: Market share data fetched from the Dune API.
    :param gas_price: Gas price data fetched from the Etherscan API.
    :param tvl: Total Value Locked (TVL) fetched from the DeFiLlama API.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            create_tables(cursor)
            timestamp = datetime.now().isoformat()

            # Insert Gas Price Data
            if gas_price:
                cursor.execute("""
                    INSERT INTO gas_price (timestamp, low, average, high)
                    VALUES (?, ?, ?, ?)
                """, (timestamp, gas_price["low"], gas_price["average"], gas_price["high"]))
                logging.info("✅ Gas price data stored successfully.")
            else:
                logging.warning("⚠ Gas price data could not be retrieved.")

            # Insert TVL Data
            if tvl:
                cursor.execute("""
                    INSERT INTO tvl (timestamp, tvl)
                    VALUES (?, ?)
                """, (timestamp, tvl))
                logging.info("✅ TVL data stored successfully.")
            else:
                logging.warning("⚠ TVL data could not be retrieved.")

            # Insert Market Share Data
            if market_data and "result" in market_data and "rows" in market_data["result"]:
                rows = market_data["result"]["rows"]
                batch_data = [
                    (
                        timestamp,
                        row.get("market"),
                        row.get("blockchain"),
                        row.get("project"),
                        row.get("version"),
                        row.get("volume_usd"),
                        row.get("trades")
                    )
                    for row in rows
                ]
                if batch_data:
                    cursor.executemany("""
                        INSERT INTO market_share (timestamp, market, blockchain, project, version, volume_usd, trades)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, batch_data)
                    logging.info(f"✅ Stored {len(batch_data)} market share records.")
                else:
                    logging.warning("⚠ No valid market share data to insert.")
            else:
                logging.warning("⚠ Market share data structure is invalid or empty.")

            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"❌ Database error: {e}")
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    logging.info("🚀 Fetching market share data...")
    market_data = fetch_market_share()

    logging.info("⛽ Fetching Ethereum gas price data...")
    gas_price_data = fetch_gas_price()

    logging.info("💰 Fetching Ethereum TVL data...")
    tvl_data = fetch_tvl()

    if market_data:
        save_to_json(market_data)
        store_market_data(market_data, gas_price_data, tvl_data)
    else:
        logging.error("❌ Failed to fetch market share data.")
