# Message to Receipt Printer

A project that allows messages submitted through a website to be printed automatically on a thermal receipt printer.

The project is designed for use cases such as:

- website guestbooks
- RSVP confirmations for events with online invitation
- party pinboard / guestbook
- DJ song requests
- interactive installations

Messages submitted through a web interface are stored in a databse on a server and retrieved by a Raspberry Pi client.  
The Raspberry Pi then prints them on a thermal receipt printer locally.

The project is currently focused on the printer client and **work-in-progress**.  
The web server component will be added later.

# Hardware

Tested with:

- Raspberry Pi
- Epson TM-T88V thermal receipt printer
- Network connection (Ethernet or LAN)

Other ESC/POS compatible printers should also work.

The project uses the Python library:

- [python-escpos](https://github.com/python-escpos/python-escpos)

# Project Structure

```

message-to-receipt-printer/
│
├─ pi-client/ # Raspberry Pi printing client
├─ web/ # future web server
├─ .env.example # environment configuration template
└─ README.md

````

# Raspberry Pi Client

The `pi-client` is responsible for:

- polling the API for new entries
- printing entries on the receipt printer
- reporting printing results back to the server

# Deployment (Raspberry Pi)

### 1. Clone the repository

```bash
git clone https://github.com/TobiLxtr/message-to-receipt-printer.git
cd message-to-receipt-printer/pi-client
````

### 2. Install uv

If `uv` is not installed yet:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Create virtual environment

```bash
uv venv
```

Activate it:

```bash
source .venv/bin/activate
uv pip install -e .
```

### 4. Install dependencies

```bash
uv pip install -e .
```

### 5. Configure environment variables

Copy the example file:

```bash
cp ../.env.example .env
```

Edit the configuration:

```bash
nano .env
```

Example configuration:

```env
PRINTER_IP=192.168.1.10
PRINTER_PROFILE=TM-T88V
```

### 6. Start the client

From inside the `pi-client` directory:

```bash
uv run receipt-printer-client
```

The client will now:

1. connect to the printer
2. poll the API for new entries
3. print entries
4. report results to the server

# Environment Variables

| Variable        | Description                                   |
| --------------- | --------------------------------------------- |
| PRINTER_IP      | IP address of the receipt printer             |
| PRINTER_PROFILE | Printer profile used by python-escpos         |
| PRINTER_PORT    | Printer port (default: 9100)                  |
| PRINTER_TIMEOUT | Network timeout in seconds (default: 5)       |
| POLL_INTERVAL   | API polling interval in seconds (default: 10) |