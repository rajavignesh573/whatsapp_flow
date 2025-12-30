# Test Your Live API on Vercel

Your API is live at: **https://whatsapp-flow-pi.vercel.app**

## Quick Test Methods

### Method 1: Using the Test Script (Easiest)

```bash
cd /home/hp/whatsapp_flow
./test_deployed_api.sh https://whatsapp-flow-pi.vercel.app
```

This will test all endpoints automatically.

---

### Method 2: Manual Testing with curl

#### 1. Health Check
```bash
curl https://whatsapp-flow-pi.vercel.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "WhatsApp Webhook API",
  "database_file": "whatsapp_messages.json",
  "users_database_file": "users.json"
}
```

#### 2. Check New User (should return exists: false)
```bash
curl -X POST https://whatsapp-flow-pi.vercel.app/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'
```

Expected response:
```json
{
  "exists": false
}
```

#### 3. Save User ⚠️ MANDATORY

**⚠️ IMPORTANT:** This step MUST happen before wishlist actions!

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

Expected response:
```json
{
  "status": "success",
  "message": "User saved successfully",
  "user": {
    "phone": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": [],
    "created_at": "...",
    "updated_at": "..."
  }
}
```

**Kapso Webhook Configuration:**
```
POST https://whatsapp-flow-pi.vercel.app/save-user

Body:
{
  "user": "{{context.phone_number}}",
  "parent_name": "{{parent_name}}",
  "child_name": "{{child_name}}",
  "wishlist": []
}

➡️ This step MUST happen before wishlist actions
```

#### 4. Check Existing User (should return exists: true)
```bash
curl -X POST https://whatsapp-flow-pi.vercel.app/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'
```

Expected response:
```json
{
  "exists": true,
  "parent_name": "John",
  "child_name": "Sarah",
  "wishlist": []
}
```

#### 5. Get All Users
```bash
curl https://whatsapp-flow-pi.vercel.app/users
```

#### 6. Get Specific User
```bash
curl https://whatsapp-flow-pi.vercel.app/users/+1234567890
```

#### 7. Test Webhook Endpoint
```bash
curl -X POST https://whatsapp-flow-pi.vercel.app/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "parent": "John",
    "child": "Sarah",
    "wishlist": ["Toy Car", "Book", "Puzzle"]
  }'
```

---

### Method 3: Using Browser (for GET requests)

Open these URLs in your browser:

- Health Check: https://whatsapp-flow-pi.vercel.app/health
- Get All Users: https://whatsapp-flow-pi.vercel.app/users
- Get User: https://whatsapp-flow-pi.vercel.app/users/+1234567890

---

### Method 4: Using Postman or Insomnia

1. **Create a new request**
2. **Set method to POST**
3. **URL:** `https://whatsapp-flow-pi.vercel.app/check-or-create-user`
4. **Headers:**
   - `Content-Type: application/json`
5. **Body (raw JSON):**
   ```json
   {
     "phone": "+1234567890"
   }
   ```
6. **Send**

---

### Method 5: Using Python Script

Create a test file `test_api.py`:

```python
import requests

API_URL = "https://whatsapp-flow-pi.vercel.app"

# Test 1: Health check
response = requests.get(f"{API_URL}/health")
print("Health Check:", response.json())

# Test 2: Check new user
response = requests.post(
    f"{API_URL}/check-or-create-user",
    json={"phone": "+1234567890"}
)
print("Check User:", response.json())

# Test 3: Save user
response = requests.post(
    f"{API_URL}/save-user",
    json={
        "user": "+1234567890",
        "parent_name": "John",
        "child_name": "Sarah",
        "wishlist": []
    }
)
print("Save User:", response.json())

# Test 4: Check existing user
response = requests.post(
    f"{API_URL}/check-or-create-user",
    json={"phone": "+1234567890"}
)
print("Check Existing User:", response.json())
```

Run it:
```bash
python3 test_api.py
```

---

## Test All Endpoints at Once

Run this command to test everything:

```bash
echo "=== Testing Live API ===" && \
echo "1. Health Check:" && \
curl -s https://whatsapp-flow-pi.vercel.app/health | python3 -m json.tool && \
echo -e "\n2. Check New User:" && \
curl -s -X POST https://whatsapp-flow-pi.vercel.app/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+9999999999"}' | python3 -m json.tool && \
echo -e "\n3. Save User:" && \
curl -s -X POST https://whatsapp-flow-pi.vercel.app/save-user \
  -H "Content-Type: application/json" \
  -d '{"user": "+9999999999", "parent_name": "Test", "child_name": "User", "wishlist": []}' | python3 -m json.tool && \
echo -e "\n4. Check Existing User:" && \
curl -s -X POST https://whatsapp-flow-pi.vercel.app/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+9999999999"}' | python3 -m json.tool
```

---

## Use in Kapso

Now you can use your live API in Kapso:

### 1. Check User Webhook
**URL:**
```
https://whatsapp-flow-pi.vercel.app/check-or-create-user
```

### 2. Save User Webhook ⚠️ MANDATORY

**⚠️ IMPORTANT:** This MUST happen before wishlist actions!

**URL:**
```
https://whatsapp-flow-pi.vercel.app/save-user
```

**Body:**
```json
{
  "user": "{{context.phone_number}}",
  "parent_name": "{{parent_name}}",
  "child_name": "{{child_name}}",
  "wishlist": []
}
```

**➡️ This step MUST happen before wishlist actions**

See `KAPSO_WEBHOOK_SETUP.md` for detailed setup instructions.

---

## Troubleshooting

**If you get "Not Found":**
- Make sure you're using the correct endpoint path
- Check that the deployment completed successfully

**If you get timeout:**
- Vercel has cold starts (first request may take 1-2 seconds)
- Subsequent requests are fast

**If you get CORS errors:**
- Add CORS to your Flask app (for browser requests)
- API-to-API calls don't need CORS

---

## Success Indicators

✅ Health check returns `{"status": "healthy"}`  
✅ Check user returns `{"exists": false}` for new numbers  
✅ Save user returns `{"status": "success"}`  
✅ Check existing user returns `{"exists": true}`  

Your API is working! 🎉

