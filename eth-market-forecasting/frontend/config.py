import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
DUNE_API_KEY = os.getenv("DUNE_API_KEY")

# Application configuration settings
DEBUG = True
DASHBOARD_UPDATE_INTERVAL = 60000  # in milliseconds
API_TIMEOUT = 10  # seconds
