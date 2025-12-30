# Save User Endpoint - Quick Reference

## Endpoint
```
POST https://whatsapp-flow-pi.vercel.app/save-user
```

---

## Request

### Headers
```
Content-Type: application/json
```

### Body
```json
{
  "user": "+1234567890",
  "parent_name": "John",
  "child_name": "Sarah",
  "wishlist": []
}
```

### Required Fields
- ✅ `user` (string) - Phone number
- ✅ `parent_name` (string) - Parent's name
- ✅ `child_name` (string) - Child's name
- ✅ `wishlist` (array) - Empty array `[]`

---

## Response

### Success (200)
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

### Error (400)
```json
{
  "status": "error",
  "message": "user is required"
}
```

---

## Quick Test

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

---

## Kapso Configuration

**URL:** `https://whatsapp-flow-pi.vercel.app/save-user`  
**Method:** `POST`  
**Body:**
```json
{
  "user": "{{context.phone_number}}",
  "parent_name": "{{parent_name}}",
  "child_name": "{{child_name}}",
  "wishlist": []
}
```

⚠️ **MUST be called before wishlist actions**

---

## Full Documentation

See `SAVE_USER_ENDPOINT.md` for complete details.

