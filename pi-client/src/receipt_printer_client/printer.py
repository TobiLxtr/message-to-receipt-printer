# src/receipt_printer_client/printer.py

from escpos.printer import Network

from receipt_printer_client.config import (
    PRINTER_IP,
    PRINTER_PORT,
    PRINTER_TIMEOUT,
    PRINTER_PROFILE,
)

from receipt_printer_client.text_sanitizer import sanitize_text, sanitize_name


# --------------------------------------------------
# Custom exceptions
# --------------------------------------------------

class PrinterConnectionError(Exception):
    """Raised when the printer connection is lost or unavailable."""
    pass


class EntryPrintError(Exception):
    """Raised when a specific entry cannot be printed."""
    pass


# --------------------------------------------------
# Printer wrapper
# --------------------------------------------------

class ReceiptPrinter:
    """
    Wrapper around python-escpos network printer.

    Responsibilities:
    - manage printer connection
    - expose printing functions
    """

    def __init__(self) -> None:
        self._printer: Network | None = None
        self._columns: dict[str, int] = {}

    # --------------------------------------------------
    # Connection handling
    # --------------------------------------------------

    def connect(self) -> bool:
        """
        Attempt to connect to the printer.

        Returns
        -------
        bool
            True if connection was successful.
        """

        try:

            self._printer = Network(
                PRINTER_IP,
                PRINTER_PORT,
                timeout=PRINTER_TIMEOUT,
                profile=PRINTER_PROFILE,
            )

            if not self._printer.is_online():
                raise PrinterConnectionError("Printer reported offline")

            print("Printer connected.")

            # Read printer font information
            fonts = self._printer.profile.profile_data.get("fonts", {})

            self._columns = {}

            for font in fonts.values():

                name = font["name"].split()[-1].lower()
                columns = font["columns"]

                self._columns[name] = columns

            print("Number of columns:", self._columns)

            return True

        except Exception as e:

            print("Printer connection failed:", e)

            self._printer = None
            return False

    def disconnect(self) -> None:
        """
        Close printer connection.
        """

        if self._printer is not None:

            try:
                self._printer.close()
            except Exception:
                pass

        self._printer = None

    def is_connected(self) -> bool:
        """
        Check if printer connection is alive.
        """

        if self._printer is None:
            return False

        try:
            return self._printer.is_online()
        except Exception:
            self.disconnect()
            return False

    # --------------------------------------------------
    # Symbol helpers
    # --------------------------------------------------

    def print_raw_symbol(self, codepage: str, byte_value: int) -> None:
        """
        Print raw symbol using specific codepage.
        """

        if not self.is_connected():
            raise PrinterConnectionError("Printer not connected")

        if not (0 <= byte_value <= 255):
            raise ValueError("byte_value must be between 0 and 255")

        self._printer.charcode(codepage)
        self._printer._raw(bytes([byte_value]))
        self._printer.charcode("AUTO")

    def print_heart(self) -> None:
        """Print heart symbol."""
        self.print_raw_symbol("CP932", 0xE9)

    # --------------------------------------------------
    # Test helpers
    # --------------------------------------------------

    def print_test(self, entry: dict) -> None:

        if not self.is_connected():
            raise PrinterConnectionError("Printer not connected")

        self.print_heart()
        self._printer.cut()

    def print_all_codepages(self) -> None:

        if not self.is_connected():
            raise PrinterConnectionError("Printer not connected")

        codepages = self._printer.profile.get_code_pages()

        for name in codepages:

            try:
                self._printer.charcode(name)
            except Exception:
                continue

            header = f"\n\nCODEPAGE: {name}\n".encode("ascii", errors="ignore")
            self._printer._raw(header)

            for i in range(256):

                self._printer._raw(bytes([i]))

                if (i + 1) % 16 == 0:
                    self._printer._raw(b"\n")

            self._printer._raw(b"\n\n")

        self._printer.cut()

    # --------------------------------------------------
    # Main formatter
    # --------------------------------------------------

    def print_website_guestbook(self, entry: dict) -> None:
        """
        Print a guestbook entry.
        """

        if not self.is_connected():
            raise PrinterConnectionError("Printer not connected")

        try:

            entry_id = entry.get("id", "UNKNOWN")
            created_at = entry.get("created_at", "")

            name = sanitize_name(entry.get("name", "Anonymous"))
            text = sanitize_text(entry.get("text", ""))

            self._printer.set(density=8)

            self._printer.set(align="center", bold=True)
            self._printer.text("WEBSITE GUESTBOOK\n")
            self._printer.text("-" * 32 + "\n\n")

            self._printer.set(align="left", bold=False)

            self._printer.text(f"ID: {entry_id}\n")
            self._printer.text(f"Time: {created_at}\n")
            self._printer.text(f"From: {name}\n\n")

            self._printer.block_text(text)
            self._printer.ln(2)

            self._printer.text("-" * 32 + "\n")

            self._printer.cut(mode='PART')

        except OSError as e:
            raise PrinterConnectionError(str(e))

        except Exception as e:
            raise EntryPrintError(str(e))