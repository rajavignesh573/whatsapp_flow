# Kapso Webhook Setup - Save User (MANDATORY)

## ⚠️ Important: This Webhook is MANDATORY

**The Save User webhook MUST be called before any wishlist actions.**

---

## 6️⃣ Webhook — Save User (MANDATORY)

### Endpoint
```
POST https://whatsapp-flow-pi.vercel.app/save-user
```

### Request Body
```json
{
  "user": "{{context.phone_number}}",
  "parent_name": "{{parent_name}}",
  "child_name": "{{child_name}}",
  "wishlist": []
}
```

### Kapso Configuration

1. **Add Step** → **Webhook**
2. **Method:** `POST`
3. **URL:** `https://whatsapp-flow-pi.vercel.app/save-user`
4. **Headers:**
   - `Content-Type: application/json`
5. **Body:**
   ```json
   {
     "user": "{{context.phone_number}}",
     "parent_name": "{{parent_name}}",
     "child_name": "{{child_name}}",
     "wishlist": []
   }
   ```

### Expected Response
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

### When to Use

- ✅ **After onboarding** (collecting parent_name and child_name)
- ✅ **Before any wishlist actions** (add item, view items, etc.)
- ✅ **When user confirms their details**

### Flow Order

```
1. Check User (check-or-create-user)
   ↓
2. Decision (is new user?)
   ↓
3. Collect parent_name and child_name
   ↓
4. ⚠️ Save User (MANDATORY) ← YOU ARE HERE
   ↓
5. Continue to wishlist actions
```

### ⚠️ Critical Notes

- **MUST be called** before wishlist operations
- **MUST include** all three fields: user, parent_name, child_name
- **wishlist** should be empty array `[]` initially
- **Failure to call this** will result in missing user data

### Test the Endpoint

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

## ✅ Checklist

- [ ] Webhook step added after onboarding
- [ ] URL set to: `https://whatsapp-flow-pi.vercel.app/save-user`
- [ ] Method set to: `POST`
- [ ] Body includes: `user`, `parent_name`, `child_name`, `wishlist`
- [ ] Placed BEFORE wishlist actions
- [ ] Tested successfully

---

**➡️ This step MUST happen before wishlist actions**

