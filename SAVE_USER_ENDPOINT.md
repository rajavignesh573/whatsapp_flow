# Save User Endpoint - Complete Documentation

## Endpoint Details

**URL:** `https://whatsapp-flow-pi.vercel.app/save-user`  
**Method:** `POST`  
**Content-Type:** `application/json`  
**Status:** ⚠️ **MANDATORY** - Must be called before wishlist actions

---

## Request

### Headers
```
Content-Type: application/json
```

### Request Body
```json
{
  "user": "+1234567890",
  "parent_name": "John",
  "child_name": "Sarah",
  "wishlist": []
}
```

### Request Body Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `user` | string | ✅ Yes | Phone number of the user | `"+1234567890"` |
| `parent_name` | string | ✅ Yes | Name of the parent | `"John"` |
| `child_name` | string | ✅ Yes | Name of the child | `"Sarah"` |
| `wishlist` | array | ✅ Yes | Initial wishlist (empty array) | `[]` |

### Request Example (cURL)
```bash
curl -X POST https://whatsapp-flow-pi.vercel.app/save-user \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": []
  }'
```

### Request Example (JavaScript/Fetch)
```javascript
fetch('https://whatsapp-flow-pi.vercel.app/save-user', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    user: '+1234567890',
    parent_name: 'John',
    child_name: 'Sarah',
    wishlist: []
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### Request Example (Python)
```python
import requests

url = "https://whatsapp-flow-pi.vercel.app/save-user"
payload = {
    "user": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": []
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

---

## Response

### Success Response (200 OK)

**Status Code:** `200`

**Response Body:**
```json
{
  "status": "success",
  "message": "User saved successfully",
  "user": {
    "phone": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": [],
    "created_at": "2025-12-30T16:18:22.038653",
    "updated_at": "2025-12-30T16:18:22.038675"
  }
}
```

### Success Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Status of the operation (`"success"`) |
| `message` | string | Success message |
| `user` | object | Saved user object |
| `user.phone` | string | User's phone number |
| `user.parent_name` | string | Parent's name |
| `user.child_name` | string | Child's name |
| `user.wishlist` | array | User's wishlist (initially empty) |
| `user.created_at` | string | ISO timestamp of creation |
| `user.updated_at` | string | ISO timestamp of last update |

---

### Error Responses

#### 400 Bad Request - Missing Required Field

**Status Code:** `400`

**Response Body:**
```json
{
  "status": "error",
  "message": "user is required"
}
```

**Possible Messages:**
- `"No data received"`
- `"user is required"`
- `"parent_name is required"`
- `"child_name is required"`

#### 500 Internal Server Error

**Status Code:** `500`

**Response Body:**
```json
{
  "status": "error",
  "message": "Error message here"
}
```

**Common Causes:**
- Database write failure
- Server error
- File system error (on Vercel - read-only filesystem)

---

## Testing

### Test 1: Basic Save User Test

```bash
curl -X POST https://whatsapp-flow-pi.vercel.app/save-user \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+9998887777",
    "parent_name": "Test Parent",
    "child_name": "Test Child",
    "wishlist": []
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "User saved successfully",
  "user": {
    "phone": "+9998887777",
    "parent_name": "Test Parent",
    "child_name": "Test Child",
    "wishlist": [],
    "created_at": "2025-12-30T...",
    "updated_at": "2025-12-30T..."
  }
}
```

---

### Test 2: Verify User Was Saved

```bash
curl https://whatsapp-flow-pi.vercel.app/users/+9998887777
```

**Expected Response:**
```json
{
  "status": "success",
  "user": {
    "phone": "+9998887777",
    "parent_name": "Test Parent",
    "child_name": "Test Child",
    "wishlist": [],
    "created_at": "2025-12-30T...",
    "updated_at": "2025-12-30T..."
  }
}
```

---

### Test 3: Update Existing User

```bash
curl -X POST https://whatsapp-flow-pi.vercel.app/save-user \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+9998887777",
    "parent_name": "Updated Parent",
    "child_name": "Updated Child",
    "wishlist": []
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "User saved successfully",
  "user": {
    "phone": "+9998887777",
    "parent_name": "Updated Parent",
    "child_name": "Updated Child",
    "wishlist": [],
    "created_at": "2025-12-30T...",
    "updated_at": "2025-12-30T..."  // New timestamp
  }
}
```

---

### Test 4: Missing Required Field (Error Test)

```bash
curl -X POST https://whatsapp-flow-pi.vercel.app/save-user \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+9998887777",
    "parent_name": "Test Parent"
  }'
```

**Expected Response:**
```json
{
  "status": "error",
  "message": "child_name is required"
}
```

---

### Test 5: Empty Request (Error Test)

```bash
curl -X POST https://whatsapp-flow-pi.vercel.app/save-user \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected Response:**
```json
{
  "status": "error",
  "message": "user is required"
}
```

---

## Complete Test Script

Save this as `test_save_user.sh`:

```bash
#!/bin/bash

API_URL="https://whatsapp-flow-pi.vercel.app"

echo "=== Testing Save User Endpoint ==="
echo ""

# Test 1: Save new user
echo "1. Saving new user..."
RESPONSE=$(curl -s -X POST "$API_URL/save-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1112223333",
    "parent_name": "Alice",
    "child_name": "Bob",
    "wishlist": []
  }')
echo "$RESPONSE" | python3 -m json.tool
echo ""

# Test 2: Verify user was saved
echo "2. Verifying user was saved..."
curl -s "$API_URL/users/+1112223333" | python3 -m json.tool
echo ""

# Test 3: Update existing user
echo "3. Updating existing user..."
RESPONSE=$(curl -s -X POST "$API_URL/save-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1112223333",
    "parent_name": "Alice Updated",
    "child_name": "Bob Updated",
    "wishlist": []
  }')
echo "$RESPONSE" | python3 -m json.tool
echo ""

# Test 4: Missing field (error test)
echo "4. Testing missing field (should error)..."
curl -s -X POST "$API_URL/save-user" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1112223333",
    "parent_name": "Test"
  }' | python3 -m json.tool
echo ""

echo "=== Tests Complete ==="
```

Run it:
```bash
chmod +x test_save_user.sh
./test_save_user.sh
```

---

## Kapso Integration

### Webhook Configuration in Kapso

1. **Step Type:** Webhook
2. **Method:** POST
3. **URL:** `https://whatsapp-flow-pi.vercel.app/save-user`
4. **Headers:**
   ```
   Content-Type: application/json
   ```
5. **Body:**
   ```json
   {
     "user": "{{context.phone_number}}",
     "parent_name": "{{parent_name}}",
     "child_name": "{{child_name}}",
     "wishlist": []
   }
   ```

### Response Handling in Kapso

The response will be stored in `{{steps.webhook.response}}`

Access fields:
- `{{steps.webhook.response.status}}` - "success" or "error"
- `{{steps.webhook.response.message}}` - Response message
- `{{steps.webhook.response.user.phone}}` - Saved phone number
- `{{steps.webhook.response.user.parent_name}}` - Saved parent name
- `{{steps.webhook.response.user.child_name}}` - Saved child name

### Flow Position

**⚠️ CRITICAL:** This endpoint MUST be called:
- ✅ After collecting `parent_name` and `child_name`
- ✅ Before any wishlist operations (add item, view items, etc.)
- ✅ After user confirms their details

**Flow Order:**
```
1. Check User → /check-or-create-user
2. Decision → Is new user?
3. Collect → parent_name, child_name
4. ⚠️ Save User → /save-user (MANDATORY)
5. Continue → Wishlist actions
```

---

## Status Codes Reference

| Status Code | Meaning | When It Occurs |
|-------------|---------|----------------|
| `200` | Success | User saved successfully |
| `400` | Bad Request | Missing required fields or invalid data |
| `500` | Server Error | Internal server error or database failure |

---

## Notes

1. **Phone Number Format:** Use international format with `+` prefix (e.g., `+1234567890`)
2. **Wishlist:** Always send empty array `[]` initially
3. **Updates:** Calling with same phone number updates existing user
4. **Timestamps:** Automatically generated in ISO format
5. **Vercel Limitation:** On Vercel, file writes may fail due to read-only filesystem. Consider using Render or a database for production.

---

## Quick Reference

**Endpoint:** `POST https://whatsapp-flow-pi.vercel.app/save-user`

**Minimal Request:**
```json
{
  "user": "+1234567890",
  "parent_name": "John",
  "child_name": "Sarah",
  "wishlist": []
}
```

**Success Response:**
```json
{
  "status": "success",
  "message": "User saved successfully",
  "user": { ... }
}
```

