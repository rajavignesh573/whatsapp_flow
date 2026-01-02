# API Testing Guide

This guide shows you how to test all API endpoints for the WhatsApp Flow application.

## Base URL
- **Production**: `https://whatsapp-flow-virid.vercel.app`
- **Local**: `http://localhost:5000` (when running locally)

---

## Quick Start

### Option 1: Python Script (Recommended)
```bash
# Install requests if not already installed
pip install requests

# Run the test script
python test_api.py
```

### Option 2: Shell Script (cURL)
```bash
# Make the script executable
chmod +x test_api.sh

# Run the test script
./test_api.sh
```

### Option 3: Manual Testing with cURL
See individual endpoint examples below.

---

## Available Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running and database is configured.

```bash
curl https://whatsapp-flow-virid.vercel.app/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "WhatsApp Webhook API",
  "database": "Supabase",
  "supabase_configured": true,
  ...
}
```

---

### 2. Debug Info
**GET** `/debug`

Get debug information about configuration.

```bash
curl https://whatsapp-flow-virid.vercel.app/debug
```

---

### 3. Save User ⭐
**POST** `/save-user`

Save or update user information.

**Request Body:**
```json
{
  "user": "+1234567890",
  "parent_name": "John Doe",
  "child_name": "Jane Doe",
  "wishlist": ["toy1", "toy2"]
}
```

**cURL Example:**
```bash
curl -X POST https://whatsapp-flow-virid.vercel.app/save-user \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1234567890",
    "parent_name": "John Doe",
    "child_name": "Jane Doe",
    "wishlist": ["toy1", "toy2"]
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "User saved successfully",
  "user": {
    "phone": "+1234567890",
    "parent_name": "John Doe",
    "child_name": "Jane Doe",
    "wishlist": ["toy1", "toy2"],
    ...
  }
}
```

---

### 4. Check or Create User
**POST** `/check-or-create-user`

Check if a user exists by phone number.

**Request Body:**
```json
{
  "phone": "+1234567890"
}
```

**cURL Example:**
```bash
curl -X POST https://whatsapp-flow-virid.vercel.app/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'
```

**Expected Response (User Exists):**
```json
{
  "exists": true,
  "parent_name": "John Doe",
  "child_name": "Jane Doe",
  "wishlist": ["toy1", "toy2"]
}
```

**Expected Response (User Doesn't Exist):**
```json
{
  "exists": false
}
```

---

### 5. Get All Users
**GET** `/users`

Retrieve all users from the database.

```bash
curl https://whatsapp-flow-virid.vercel.app/users
```

**Expected Response:**
```json
{
  "status": "success",
  "count": 2,
  "users": {
    "+1234567890": {
      "phone": "+1234567890",
      "parent_name": "John Doe",
      ...
    },
    ...
  }
}
```

---

### 6. Get User by Phone
**GET** `/users/<phone>`

Retrieve a specific user by phone number.

```bash
curl https://whatsapp-flow-virid.vercel.app/users/+1234567890
```

**Expected Response:**
```json
{
  "status": "success",
  "user": {
    "phone": "+1234567890",
    "parent_name": "John Doe",
    "child_name": "Jane Doe",
    ...
  }
}
```

---

### 7. Get All Messages
**GET** `/messages`

Retrieve all stored WhatsApp messages.

```bash
curl https://whatsapp-flow-virid.vercel.app/messages
```

**Expected Response:**
```json
{
  "status": "success",
  "count": 5,
  "messages": [
    {
      "id": 1,
      "data": {...},
      "timestamp": "2024-01-01T12:00:00"
    },
    ...
  ]
}
```

---

### 8. Get Message by ID
**GET** `/messages/<id>`

Retrieve a specific message by ID.

```bash
curl https://whatsapp-flow-virid.vercel.app/messages/1
```

---

### 9. Webhook (POST)
**POST** `/webhook`

Receive WhatsApp webhook messages.

**Request Body:**
```json
{
  "entry": [{
    "changes": [{
      "value": {
        "messages": [{
          "from": "+1234567890",
          "text": {"body": "Hello"}
        }]
      }
    }]
  }]
}
```

**cURL Example:**
```bash
curl -X POST https://whatsapp-flow-virid.vercel.app/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "messages": [{
            "from": "+1234567890",
            "text": {"body": "Test message"}
          }]
        }
      }]
    }]
  }'
```

---

### 10. Webhook Verification (GET)
**GET** `/webhook`

Verify webhook subscription (used by WhatsApp).

```bash
curl "https://whatsapp-flow-virid.vercel.app/webhook?hub.mode=subscribe&hub.verify_token=your_verify_token_here&hub.challenge=test_challenge"
```

---

## Testing with Python requests

```python
import requests

BASE_URL = "https://whatsapp-flow-virid.vercel.app"

# Test save-user endpoint
response = requests.post(
    f"{BASE_URL}/save-user",
    json={
        "user": "+1234567890",
        "parent_name": "John Doe",
        "child_name": "Jane Doe",
        "wishlist": ["toy1", "toy2"]
    }
)

print(response.status_code)
print(response.json())
```

---

## Testing with Postman

1. Import the collection (if available)
2. Set the base URL variable
3. Run individual requests or the entire collection

---

## Common Issues

### 1. Connection Errors
- Check if the server is running
- Verify the BASE_URL is correct
- Check network connectivity

### 2. 500 Internal Server Error
- Check if Supabase is configured correctly
- Verify database tables exist (run `supabase_setup.sql`)
- Check server logs for detailed error messages

### 3. 400 Bad Request
- Verify request body format is correct
- Check required fields are included
- Ensure Content-Type header is set to `application/json`

### 4. 404 Not Found
- Verify the endpoint URL is correct
- Check if the route exists in `app.py`

---

## Local Testing

To test locally:

1. Start the Flask server:
```bash
python app.py
```

2. Update the BASE_URL in test scripts:
```python
BASE_URL = "http://localhost:5000"
```

3. Run the tests:
```bash
python test_api.py
```

---

## Tips

- Use `jq` to format JSON responses: `curl ... | jq '.'`
- Use `-v` flag with cURL for verbose output
- Check the `/health` endpoint first to verify the API is running
- Use `/debug` endpoint to check configuration status

