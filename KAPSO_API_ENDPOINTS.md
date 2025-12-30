# Kapso Flow API Endpoints

This document describes the API endpoints required for the Kapso WhatsApp onboarding flow.

## Database Structure

- **`whatsapp_messages.json`** - Stores all incoming WhatsApp messages
- **`users.json`** - Stores user information (phone, parent_name, child_name, wishlist)

## API Endpoints

### 1. Check or Create User

**Endpoint:** `POST /check-or-create-user`

**Purpose:** Check if a user exists in the database. Used by Kapso to determine if user is new or existing.

**Request Body:**
```json
{
  "phone": "+1234567890"
}
```

**Response (New User):**
```json
{
  "exists": false
}
```

**Response (Existing User):**
```json
{
  "exists": true,
  "parent_name": "John",
  "child_name": "Sarah",
  "wishlist": []
}
```

**Usage in Kapso:**
- Add Step → Webhook
- Method: POST
- URL: `YOUR_API_URL/check-or-create-user`
- Body: `{"phone": "{{context.phone_number}}"}`

---

### 2. Save User

**Endpoint:** `POST /save-user`

**Purpose:** Save or update user information after onboarding.

**Request Body:**
```json
{
  "user": "+1234567890",
  "parent_name": "John",
  "child_name": "Sarah",
  "wishlist": []
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User saved successfully",
  "user": {
    "phone": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": [],
    "created_at": "2025-12-30T10:00:00",
    "updated_at": "2025-12-30T10:00:00"
  }
}
```

**Usage in Kapso:**
- Add Step → Webhook
- Method: POST
- URL: `YOUR_API_URL/save-user`
- Body:
```json
{
  "user": "{{context.phone_number}}",
  "parent_name": "{{parent_name}}",
  "child_name": "{{child_name}}",
  "wishlist": []
}
```

---

### 3. Get All Users

**Endpoint:** `GET /users`

**Purpose:** Retrieve all users from the database.

**Response:**
```json
{
  "status": "success",
  "count": 2,
  "users": {
    "+1234567890": {
      "phone": "+1234567890",
      "parent_name": "John",
      "child_name": "Sarah",
      "wishlist": [],
      "created_at": "2025-12-30T10:00:00",
      "updated_at": "2025-12-30T10:00:00"
    }
  }
}
```

---

### 4. Get User by Phone

**Endpoint:** `GET /users/<phone>`

**Purpose:** Retrieve a specific user by phone number.

**Example:** `GET /users/+1234567890`

**Response:**
```json
{
  "status": "success",
  "user": {
    "phone": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": [],
    "created_at": "2025-12-30T10:00:00",
    "updated_at": "2025-12-30T10:00:00"
  }
}
```

---

## Complete Kapso Flow Integration

### Step 1: Check User
```
Webhook → POST /check-or-create-user
Body: {"phone": "{{context.phone_number}}"}
```

### Step 2: Decision
```
Decision → {{steps.webhook.response.exists}} == false
```

### Step 3: New User Flow
After collecting parent_name and child_name:
```
Webhook → POST /save-user
Body: {
  "user": "{{context.phone_number}}",
  "parent_name": "{{parent_name}}",
  "child_name": "{{child_name}}",
  "wishlist": []
}
```

---

## Testing

Run the test script:
```bash
./test_kapso_endpoints.sh
```

Or test manually:

```bash
# Check new user
curl -X POST http://localhost:5000/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'

# Save user
curl -X POST http://localhost:5000/save-user \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": []
  }'

# Check existing user
curl -X POST http://localhost:5000/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'
```

---

## Data Storage

Users are stored in `users.json` with the following structure:
```json
{
  "+1234567890": {
    "phone": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": [],
    "created_at": "2025-12-30T10:00:00",
    "updated_at": "2025-12-30T10:00:00"
  }
}
```

