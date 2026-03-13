# src/receipt_printer_client/api_client.py

import requests
from typing import Dict, List, Any

from receipt_printer_client.config import (
    API_BASE_URL,
    API_KEY,
    EVENT_PUBLIC_ID,
)

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
}


# --------------------------------------------------
# Fetch entries
# --------------------------------------------------

def fetch_new_entries() -> Dict[str, Any]:
    """
    Retrieve new entries from the API.

    Raises
    ------
    RuntimeError
        If the request fails or the response is invalid.
    """

    url = f"{API_BASE_URL}/api/get_entries.php"

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            params={"event": EVENT_PUBLIC_ID},
            timeout=10,
        )

        response.raise_for_status()

    except requests.exceptions.RequestException as e:

        raise RuntimeError(
            f"API request failed while fetching entries: {e}"
        ) from e

    try:

        data = response.json()

    except ValueError as e:

        raise RuntimeError(
            f"Failed to parse API JSON response from {url}"
        ) from e

    if not isinstance(data, dict):

        raise RuntimeError(
            "Invalid API response format (expected JSON object)"
        )

    return data


# --------------------------------------------------
# Report print results
# --------------------------------------------------

def report_print_results(
    printed_ids: List[str],
    failed: List[Dict[str, Any]],
) -> None:
    """
    Send printing results back to the API.

    Raises
    ------
    RuntimeError
        If the request fails.
    """

    url = f"{API_BASE_URL}/api/report_print_results.php"

    payload = {
        "event": EVENT_PUBLIC_ID,
        "printed_ids": printed_ids,
        "failed": failed,
    }

    try:

        response = requests.post(
            url,
            headers=HEADERS,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

    except requests.exceptions.RequestException as e:

        raise RuntimeError(
            f"API request failed while reporting results: {e}"
        ) from e