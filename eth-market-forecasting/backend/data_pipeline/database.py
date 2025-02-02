import sqlite3
import json
import logging
from datetime import datetime

# Database Path
DB_PATH = "backend/data_pipeline/market_data.db"
JSON_PATH = "backend/data_pipeline/market_share_data.json"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


### 📌 1️⃣ Create Required Tables
def create_tables():
    """
    Creates necessary database tables for market share, ETH price, and gas price data.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create Market Share Table
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

        # Create ETH Price Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eth_price (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                price REAL
            )
        """)

        # Create Gas Price Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gas_price (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                low REAL,
                average REAL,
                high REAL
            )
        """)

        conn.commit()
        logging.info("✅ Database tables verified/created successfully.")

    except sqlite3.Error as e:
        logging.error(f"❌ Database error: {e}")
    finally:
        conn.close()


### 📌 2️⃣ Store Market Share Data from JSON
def store_market_data():
    """
    Reads market share data from JSON and stores it in the database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Load Market Data JSON
        try:
            with open(JSON_PATH, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"❌ Error loading JSON data: {e}")
            return

        # Insert Market Share Data
        if "result" in data and "rows" in data["result"]:
            rows = data["result"]["rows"]
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

            conn.commit()
            logging.info(f"✅ Stored {len(batch_data)} market share records.")
        else:
            logging.warning("⚠ No valid market share data found in JSON.")

    except sqlite3.Error as e:
        logging.error(f"❌ Database error: {e}")
    finally:
        conn.close()


### 📌 3️⃣ Store ETH & Gas Prices
def store_eth_price(price):
    """
    Stores Ethereum price data into the database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO eth_price (timestamp, price) VALUES (?, ?)", 
                       (datetime.now(), price))

        conn.commit()
        logging.info("✅ ETH price data stored successfully.")

    except sqlite3.Error as e:
        logging.error(f"❌ Database error: {e}")
    finally:
        conn.close()


def store_gas_price(low, average, high):
    """
    Stores Ethereum gas price data into the database.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO gas_price (timestamp, low, average, high) VALUES (?, ?, ?, ?)", 
                       (datetime.now(), low, average, high))

        conn.commit()
        logging.info("✅ Gas price data stored successfully.")

    except sqlite3.Error as e:
        logging.error(f"❌ Database error: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    logging.info("🚀 Running database setup and data storage process...")
    create_tables()
    store_market_data()
