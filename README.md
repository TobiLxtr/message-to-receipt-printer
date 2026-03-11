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

## Deployment (Raspberry Pi)

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

## Environment Variables

| Variable        | Description                                   |
| --------------- | --------------------------------------------- |
| PRINTER_IP      | IP address of the receipt printer             |
| PRINTER_PROFILE | Printer profile used by python-escpos         |
| PRINTER_PORT    | Printer port (default: 9100)                  |
| PRINTER_TIMEOUT | Network timeout in seconds (default: 5)       |
| POLL_INTERVAL   | API polling interval in seconds (default: 10) |


# Web Server

The `web` directory contains the PHP web server responsible for:

- receiving messages submitted through the website
- storing messages in a MySQL database
- providing an API for the Raspberry Pi client
- managing events and message queues

The web server is designed to run on standard shared hosting environments such as **cPanel** with:

- PHP 8+
- MySQL / MariaDB
- PDO and pdo_mysql extensions

No framework is required.

## Web Server Structure

```
web/
│
├─ api/                     # API endpoints used by the Raspberry Pi client
│
├─ config/                  # configuration and database connection
│  ├─ config.example.php
│  ├─ config.php            # not tracked by git
│  └─ database.php
│
├─ lib/                     # helper functions (auth, responses, rate limiting)
│
├─ public/                  # public web pages
│  ├─ index.php
│  ├─ event.php
│  └─ submit.php
│
├─ sql/                     # database commands
│  ├─ create_event.sql
│  └─ schema.sql
│
└─ uploads/                 # image uploads (future feature)
```

## Deployment (Web Server)

Upload the contents of the `web/` directory to your web host using FTP.

Example target directory:

```
public_html/receipt-printer/
```

Example structure on the server:

```
public_html
└─ receipt-printer
   ├─ api/
   ├─ config/
   ├─ lib/
   ├─ public/
   ├─ sql/
   └─ uploads/
```

Your event page will then be available at:

```
[https://your-domain.com/receipt-printer/public/event.php?event=EVENT_ID](https://your-domain.com/receipt-printer/public/event.php?event=EVENT_ID)
```

## Database Setup

### 1. Create a database

Create a MySQL database using your hosting control panel.

Example:

```
user_receipt_printer
```

Also create a database user and grant full access to the database.

### 2. Import database commands

Open **phpMyAdmin**, select your database and insert:

```
web/sql/schema.sql
```

This will create the required tables:

```
events
entries
```

Both tables use **utf8mb4** encoding to support:

- emojis
- international characters
- extended Unicode symbols

## Configuration

The web server uses a configuration file containing:

- database credentials
- API key
- rate limiting settings

### Create config.php

Copy the example configuration:

```
cp config/config.example.php config/config.php
```

Then edit the file and adjust the settings:

```
nano config/config.php
````

Example configuration:

```php
define("DB_HOST", "localhost");
define("DB_NAME", "user_receipt_printer");
define("DB_USER", "db_user");
define("DB_PASS", "db_password");

define("API_KEY", "your-secret-api-key");

define("RATE_LIMIT_MAX_MESSAGES", 10);
define("RATE_LIMIT_WINDOW_SECONDS", 3600);
````

## Creating an Event

Events define where messages belong.

Each event has a **public ID** used in URLs and QR codes.

Example SQL command (sql/create_event.sql):

```sql
INSERT INTO events
(public_id, slug, name, type, created_at)
VALUES
(
    'insert-public-id',
    'test-event',
    'Test Event',
    'website-guestbook',
    NOW()
);
```

## Event URL

Visitors can submit messages using the event URL:

```
https://your-domain.com/receipt-printer/public/event.php?event=insert-public-id
```

This page provides a simple form where users can enter:

* name
* message

Messages are stored in the database and later retrieved by the Raspberry Pi client.

## API

The Raspberry Pi client communicates with the web server through two API endpoints.

All API requests require the **API key** sent via HTTP header:

```
X-API-Key: YOUR_API_KEY
```

### Retrieve new entries

```
GET /api/get_entries.php?event=insert-public-id
```

Example:

```
https://your-domain.com/receipt-printer/api/get_entries.php?event=insert-public-id
```

Returns:

```json
{
  "type": "website-guestbook",
  "entries": [
    {
      "id": 1,
      "created_at": "2026-03-11 20:00:00",
      "name": "John",
      "text": "Hello world",
      "image_url": null
    }
  ]
}
```

### Report print results

```
POST /api/report_print_results.php
```

Example request body:

```json
{
  "event": "insert-public-id",
  "printed_ids": [1,2],
  "failed": [
    {
      "id": 3,
      "error": "Image too large"
    }
  ]
}
```

### Rate Limiting

To prevent spam, the server limits the number of messages per IP address.

Default configuration:

```
10 messages per IP within 60 minutes
```

These limits can be adjusted in:

```
config/config.php
```

# Current Status

The project is currently functional but still under active development.

Planned improvements include:

* image uploads
* event management interface
* printable receipt preview in the web interface
* QR code generation for event links