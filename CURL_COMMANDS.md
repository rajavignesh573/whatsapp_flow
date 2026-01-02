# cURL Testing Commands

Ready-to-use cURL commands for testing all API endpoints.

**Base URL:** `https://whatsapp-flow-virid.vercel.app`  
**Local URL:** `http://localhost:5000` (when running locally)

---

## 1. Health Check

```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/health"
```

**With formatted output:**
```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/health" | jq '.'
```

---

## 2. Debug Info

```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/debug"
```

**With formatted output:**
```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/debug" | jq '.'
```

---

## 3. Save User ⭐

```bash
curl -X POST "https://whatsapp-flow-virid.vercel.app/save-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1234567890",
    "parent_name": "John Doe",
    "child_name": "Jane Doe",
    "wishlist": ["toy1", "toy2"]
  }'
```

**One-liner version:**
```bash
curl -X POST "https://whatsapp-flow-virid.vercel.app/save-user" -H "Content-Type: application/json" -d '{"user": "+1234567890", "parent_name": "John Doe", "child_name": "Jane Doe", "wishlist": ["toy1", "toy2"]}'
```

**With formatted output:**
```bash
curl -X POST "https://whatsapp-flow-virid.vercel.app/save-user" \
  -H "Content-Type: application/json" \
  -d '{"user": "+1234567890", "parent_name": "John Doe", "child_name": "Jane Doe", "wishlist": ["toy1", "toy2"]}' | jq '.'
```

---

## 4. Check or Create User

```bash
curl -X POST "https://whatsapp-flow-virid.vercel.app/check-or-create-user" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'
```

**One-liner:**
```bash
curl -X POST "https://whatsapp-flow-virid.vercel.app/check-or-create-user" -H "Content-Type: application/json" -d '{"phone": "+1234567890"}'
```

---

## 5. Get All Users

```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/users"
```

**With formatted output:**
```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/users" | jq '.'
```

---

## 6. Get User by Phone

```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/users/+1234567890"
```

**URL-encoded phone number (if needed):**
```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/users/%2B1234567890"
```

---

## 7. Get All Messages

```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/messages"
```

**With formatted output:**
```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/messages" | jq '.'
```

---

## 8. Get Message by ID

```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/messages/1"
```

**With formatted output:**
```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/messages/1" | jq '.'
```

---

## 9. Webhook POST

```bash
curl -X POST "https://whatsapp-flow-virid.vercel.app/webhook" \
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

**One-liner:**
```bash
curl -X POST "https://whatsapp-flow-virid.vercel.app/webhook" -H "Content-Type: application/json" -d '{"entry": [{"changes": [{"value": {"messages": [{"from": "+1234567890", "text": {"body": "Test message"}}]}}]}]}'
```

---

## 10. Webhook Verification (GET)

```bash
curl -X GET "https://whatsapp-flow-virid.vercel.app/webhook?hub.mode=subscribe&hub.verify_token=your_verify_token_here&hub.challenge=test_challenge"
```

---

## Quick Test - Save User Endpoint

**Test the `/save-user` endpoint specifically:**

```bash
curl -X POST "https://whatsapp-flow-virid.vercel.app/save-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1234567890",
    "parent_name": "John Doe",
    "child_name": "Jane Doe",
    "wishlist": ["toy1", "toy2"]
  }' \
  -w "\n\nHTTP Status: %{http_code}\n"
```

---

## Tips for Better Output

### 1. Pretty print JSON (requires `jq`):
```bash
curl ... | jq '.'
```

### 2. Show HTTP status code:
```bash
curl ... -w "\nHTTP Status: %{http_code}\n"
```

### 3. Verbose output (see headers):
```bash
curl -v ...
```

### 4. Save response to file:
```bash
curl ... -o response.json
```

### 5. Combined (pretty + status):
```bash
curl ... | jq '.' && echo "HTTP Status: $(curl -s -o /dev/null -w '%{http_code}' ...)"
```

---

## Example: Complete Test with All Options

```bash
curl -X POST "https://whatsapp-flow-virid.vercel.app/save-user" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "user": "+1234567890",
    "parent_name": "John Doe",
    "child_name": "Jane Doe",
    "wishlist": ["toy1", "toy2"]
  }' \
  -w "\n\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n" \
  -v | jq '.'
```

---

## Testing Locally

If running locally on port 5000:

```bash
curl -X POST "http://localhost:5000/save-user" \
  -H "Content-Type: application/json" \
  -d '{"user": "+1234567890", "parent_name": "John Doe", "child_name": "Jane Doe", "wishlist": ["toy1", "toy2"]}'
```

