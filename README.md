# WhatsApp Webhook API

A simple Flask API to receive and store WhatsApp messages using JSON as a database.

## Features

- Receive WhatsApp webhook messages via POST requests
- Store all messages in a JSON file (`whatsapp_messages.json`)
- Webhook verification endpoint for WhatsApp setup
- Retrieve all messages or specific message by ID
- Health check endpoint

## Installation

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Activate virtual environment (if using one):
```bash
source venv/bin/activate
```

2. Start the server:
```bash
python3 app.py
```

The server will run on `http://0.0.0.0:5000`

## API Endpoints

### POST /webhook
Receive WhatsApp messages and store them in JSON database.

**Request Body:** Any JSON data from WhatsApp API

**Response:**
```json
{
  "status": "success",
  "message": "Message received and stored",
  "received_at": "2024-01-01T12:00:00"
}
```

### GET /webhook
Webhook verification endpoint for WhatsApp setup.

**Query Parameters:**
- `hub.mode`: Should be "subscribe"
- `hub.verify_token`: Your verification token
- `hub.challenge`: Challenge string from WhatsApp

### GET /messages
Retrieve all stored messages.

**Response:**
```json
{
  "status": "success",
  "count": 10,
  "messages": [...]
}
```

### GET /messages/<id>
Retrieve a specific message by ID.

### GET /health
Health check endpoint.

## Configuration

Set the `WHATSAPP_VERIFY_TOKEN` environment variable for webhook verification:
```bash
export WHATSAPP_VERIFY_TOKEN=your_secret_token
```

## Data Storage

All messages are stored in `whatsapp_messages.json` with the following structure:
- Each message gets an auto-incremented `id`
- Each message gets a `timestamp` (ISO format)
- Original WhatsApp data is preserved

## Example Webhook Payload

When WhatsApp sends a message, it will be stored with this structure:
```json
{
  "id": 1,
  "timestamp": "2024-01-01T12:00:00.123456",
  "entry": [...],
  "object": "whatsapp_business_account"
}
```

