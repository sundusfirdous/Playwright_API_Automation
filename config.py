import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Selected environment
ENV = os.getenv("ENV", "qa").lower()

# Dynamically select Base URL
BASE_URL = os.getenv(f"{ENV.upper()}_BASE_URL")

# Credentials
USERNAME = os.getenv(f"{ENV.upper()}_USERNAME")
PASSWORD = os.getenv(f"{ENV.upper()}_PASSWORD")

# Validate configuration
if not BASE_URL:
    raise ValueError(f"Base URL not configured for {ENV} environment")

if not USERNAME or not PASSWORD:
    raise ValueError(f"Credentials not configured for {ENV} environment")