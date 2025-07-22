import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# API Keys
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
DUNE_API_KEY = os.getenv("DUNE_API_KEY", "")

# Application Configuration Settings
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
DASHBOARD_UPDATE_INTERVAL = int(os.getenv("DASHBOARD_UPDATE_INTERVAL", 60000))  # in milliseconds
API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10))  # seconds
