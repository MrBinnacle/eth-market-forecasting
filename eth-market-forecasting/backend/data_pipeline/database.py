import sqlite3
import json
import logging
from datetime import datetime

# Database and JSON file paths
DB_PATH = "backend/data_pipeline/market_data.db"
JSON_PATH = "backend/data_pipeline/market_share_data.json"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_tables():
    """
    Creates necessary database tables for market share, ETH price, gas price, and TVL.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
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
                CREATE TABLE IF NOT EXISTS eth_price (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    price REAL
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
            conn.commit()
            logging.info("✅ Database tables verified/created successfully.")
    except sqlite3.Error as e:
        logging.error(f"❌ Database error during table creation: {e}")


def store_market_data():
    """
    Reads market share data from JSON and stores it in the database.
    """
    try:
        with open(JSON_PATH, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"❌ Error loading JSON data: {e}")
        return

    if "result" in data and "rows" in data["result"]:
        rows = data["result"]["rows"]
        timestamp = datetime.now().isoformat()
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
            for row in rows if row.get("volume_usd") is not None  # Ensure valid data
        ]

        if batch_data:
            try:
                with sqlite3.connect(DB_PATH) as conn:
                    cursor = conn.cursor()
                    cursor.executemany("""
                        INSERT INTO market_share (timestamp, market, blockchain, project, version, volume_usd, trades)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, batch_data)
                    conn.commit()
                    logging.info(f"✅ Stored {len(batch_data)} market share records.")
            except sqlite3.Error as e:
                logging.error(f"❌ Database error while storing market share data: {e}")
        else:
            logging.warning("⚠ No valid market share data to insert.")
    else:
        logging.warning("⚠ No valid market share data found in JSON.")


def store_eth_price(price):
    """
    Stores Ethereum price data into the database.

    :param price: ETH price as a float.
    """
    if price is None:
        logging.warning("⚠ Skipping ETH price storage due to missing data.")
        return

    timestamp = datetime.now().isoformat()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO eth_price (timestamp, price) VALUES (?, ?)", (timestamp, price))
            conn.commit()
            logging.info("✅ ETH price data stored successfully.")
    except sqlite3.Error as e:
        logging.error(f"❌ Database error while storing ETH price: {e}")


def store_gas_price(low, average, high):
    """
    Stores Ethereum gas price data into the database.

    :param low: Low gas price.
    :param average: Average gas price.
    :param high: High gas price.
    """
    if None in (low, average, high):
        logging.warning("⚠ Skipping gas price storage due to missing data.")
        return

    timestamp = datetime.now().isoformat()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gas_price (timestamp, low, average, high) VALUES (?, ?, ?, ?)",
                (timestamp, low, average, high)
            )
            conn.commit()
            logging.info("✅ Gas price data stored successfully.")
    except sqlite3.Error as e:
        logging.error(f"❌ Database error while storing gas price: {e}")


def store_tvl(tvl):
    """
    Stores Ethereum Total Value Locked (TVL) data into the database.

    :param tvl: TVL in USD.
    """
    if tvl is None:
        logging.warning("⚠ Skipping TVL storage due to missing data.")
        return

    timestamp = datetime.now().isoformat()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tvl (timestamp, tvl) VALUES (?, ?)", (timestamp, tvl))
            conn.commit()
            logging.info("✅ TVL data stored successfully.")
    except sqlite3.Error as e:
        logging.error(f"❌ Database error while storing TVL: {e}")


if __name__ == "__main__":
    logging.info("🚀 Running database setup and data storage process...")
    create_tables()
    store_market_data()
