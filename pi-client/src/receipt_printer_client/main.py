# src/receipt_printer_client/main.py

import time
import traceback
from typing import List

from receipt_printer_client.api_client import (
    fetch_new_entries,
    report_print_results
)

from receipt_printer_client.printer import (
    ReceiptPrinter,
    PrinterConnectionError,
    EntryPrintError
)

from receipt_printer_client.config import POLL_INTERVAL


def main() -> None:
    """
    Main polling loop.

    Workflow:

    1. Ensure printer connection
    2. Fetch entries from API
    3. Print entries
    4. Report results to API
    """

    printer = ReceiptPrinter()

    print(f"Starting polling loop (interval {POLL_INTERVAL}s)")

    while True:

        try:

            # --------------------------------------------------
            # Ensure printer connection
            # --------------------------------------------------

            if not printer.is_connected():

                print("Printer not connected. Attempting reconnect...")

                if not printer.connect():
                    time.sleep(POLL_INTERVAL)
                    continue

            # --------------------------------------------------
            # Fetch entries
            # --------------------------------------------------

            data = fetch_new_entries()

            entry_type = data.get("type")
            entries = data.get("entries", [])

            if not entries:
                time.sleep(POLL_INTERVAL)
                continue

            printed_ids: List[str] = []
            failed: List[dict] = []

            # --------------------------------------------------
            # Print entries
            # --------------------------------------------------

            for entry in entries:

                entry_id = entry.get("id", "UNKNOWN")

                if not printer.is_connected():
                    print("Printer disconnected during printing.")
                    break

                try:

                    match entry_type:

                        case "website-guestbook":
                            print("Printing guestbook entry:", entry_id)
                            printer.print_website_guestbook(entry)

                        case "test":
                            printer.print_test(entry)

                        case "codepages":
                            printer.print_all_codepages()

                        case "empty":
                            print("Empty message printed.")
                            pass

                        case _:
                            print("Unsupported entry type:", entry_type)
                            failed.append({
                                "id": entry_id,
                                "error": f"Unsupported entry type: {entry_type}"
                            })
                            continue

                    printed_ids.append(entry_id)

                except PrinterConnectionError:

                    print("Printer connection lost.")
                    printer.disconnect()

                    # Abort batch so entries are retried later
                    break

                except EntryPrintError as e:

                    print(f"Entry {entry_id} cannot be printed:", e)

                    failed.append({
                        "id": entry_id,
                        "error": str(e)
                    })

                except Exception as e:

                    print("Unexpected error for entry:", entry_id)
                    traceback.print_exc()

                    failed.append({
                        "id": entry_id,
                        "error": str(e)
                    })

            # --------------------------------------------------
            # Report results
            # --------------------------------------------------

            if printed_ids or failed:

                try:
                    report_print_results(
                        printed_ids=printed_ids,
                        failed=failed
                    )
                except Exception:
                    print("Failed to report print results.")
                    traceback.print_exc()

            time.sleep(POLL_INTERVAL)

        except Exception as e:

            print("Unexpected error in main loop:", e)
            traceback.print_exc()

            printer.disconnect()

            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        print("\nShutdown requested.")