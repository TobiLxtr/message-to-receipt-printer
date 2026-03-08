# src/receipt_printer_client/api_client.py

import json
from typing import List, Dict, Any


def fetch_new_entries() -> Dict[str, Any]:
    """
    Simulate fetching new guestbook entries from the API.

    Later this function can be replaced with a real HTTP GET request.
    """

    # --- Simulated API response ---
    raw_json = """
    {
        "type": "empty",
        "entries": [
            {
                "id": "000001",
                "created_at": "2026-03-02T18:48:50Z",
                "name": "Joe Public",
                "text": "Hello world! ☺️❤️😄😘💔"
            }
        ]
    }
    """

    data = json.loads(raw_json)
    return data


def report_print_results(printed_ids: List[str], failed: List[Dict[str, str]]) -> None:
    """
    Report printing results to the API.

    Parameters
    ----------
    printed_ids : list[str]
        IDs of entries that were successfully printed.

    failed : list[dict]
        Entries that failed to print with error messages.
    """

    payload = {
        "printed_ids": printed_ids,
        "failed": failed
    }

    # Simulated API request
    print("Reporting print results to API:")
    print(json.dumps(payload, indent=4))
    #print(payload)

    # Later replaced with real HTTP request
    #
    # response = requests.post(API_URL, json=payload)
    # response.raise_for_status()