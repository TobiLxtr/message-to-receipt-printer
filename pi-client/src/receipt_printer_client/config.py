# src/receipt_printer_client/config.py

import os
from dotenv import load_dotenv


# Load environment variables from .env file located in the project root
load_dotenv()

# --------------------------------------------------
# Printer configuration
# --------------------------------------------------
PRINTER_IP: str | None = os.getenv("PRINTER_IP")

if not PRINTER_IP:
    raise RuntimeError(
        "PRINTER_IP is not set. Please define it in the .env file."
    )

PRINTER_PORT: int = int(os.getenv("PRINTER_PORT", "9100"))
PRINTER_TIMEOUT: int = int(os.getenv("PRINTER_TIMEOUT", "5"))
PRINTER_PROFILE: str | None = os.getenv("PRINTER_PROFILE")

# --------------------------------------------------
# API configuration
# --------------------------------------------------

API_BASE_URL: str | None = os.getenv("API_BASE_URL")
API_KEY: str | None = os.getenv("API_KEY")
EVENT_PUBLIC_ID: str | None = os.getenv("EVENT_PUBLIC_ID")

if not API_BASE_URL:
    raise RuntimeError("API_BASE_URL must be defined in .env")

if not API_KEY:
    raise RuntimeError("API_KEY must be defined in .env")

if not EVENT_PUBLIC_ID:
    raise RuntimeError("EVENT_PUBLIC_ID must be defined in .env")

# --------------------------------------------------
# Client behaviour
# --------------------------------------------------
POLL_INTERVAL: int = int(os.getenv("POLL_INTERVAL", "10"))