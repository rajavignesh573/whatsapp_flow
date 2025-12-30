# Fix: "Read-only file system" Error on Vercel

## Problem

You're getting this error:
```
[Errno 30] Read-only file system: 'users.json'
```

**Cause:** Vercel doesn't have the Supabase environment variables, so the app is falling back to JSON files (which don't work on Vercel).

---

## ✅ Solution: Add Environment Variables to Vercel

### Step 1: Go to Vercel Dashboard

1. Go to: https://vercel.com/dashboard
2. Click on your project: `whatsapp-flow` (or your project name)
3. Go to **Settings** → **Environment Variables**

### Step 2: Add SUPABASE_URL

1. Click **Add New**
2. **Name:** `SUPABASE_URL`
3. **Value:** `https://huyzlryubollexkuykgd.supabase.co`
4. **Environment:** Select all (Production, Preview, Development)
5. Click **Save**

### Step 3: Add SUPABASE_KEY

1. Click **Add New** again
2. **Name:** `SUPABASE_KEY`
3. **Value:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh1eXpscnl1Ym9sbGV4a3V5a2dkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcwOTE2NTUsImV4cCI6MjA4MjY2NzY1NX0.709TKB1MZbLXLb210KSe4nj4cHhgwK9jDZWhdFOL6fY`
4. **Environment:** Select all (Production, Preview, Development)
5. Click **Save**

### Step 4: Redeploy

After adding the variables:

1. Go to **Deployments** tab
2. Click the **three dots** (⋯) on the latest deployment
3. Click **Redeploy**
4. Or push a new commit to trigger auto-deploy

---

## ✅ Verify It's Fixed

### Test Health Endpoint

```bash
curl https://whatsapp-flow-pi.vercel.app/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "WhatsApp Webhook API",
  "database": "Supabase",
  "supabase_configured": true
}
```

If you see `"supabase_configured": true`, it's working!

### Test Save User

```bash
curl -X POST https://whatsapp-flow-pi.vercel.app/save-user \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+12083619838",
    "parent_name": "raja",
    "child_name": "sara",
    "wishlist": []
  }'
```

Should return:
```json
{
  "status": "success",
  "message": "User saved successfully",
  "user": {
    "phone": "+12083619838",
    "parent_name": "raja",
    "child_name": "sara",
    "wishlist": [],
    ...
  }
}
```

---

## 📋 Checklist

- [ ] Added `SUPABASE_URL` to Vercel environment variables
- [ ] Added `SUPABASE_KEY` to Vercel environment variables
- [ ] Selected all environments (Production, Preview, Development)
- [ ] Redeployed the application
- [ ] Tested health endpoint (shows `supabase_configured: true`)
- [ ] Tested save-user endpoint (works without errors)
- [ ] Verified data appears in Supabase dashboard

---

## 🚨 Important Notes

1. **Environment Variables Must Be Set:** Without these, the app falls back to JSON files which don't work on Vercel.

2. **Redeploy Required:** After adding environment variables, you MUST redeploy for them to take effect.

3. **Check Supabase Tables:** Make sure you've run the SQL setup script in Supabase to create the tables.

---

## ✅ After Fix

Once environment variables are set and you redeploy:
- ✅ No more "read-only file system" errors
- ✅ Data saves to Supabase
- ✅ Works perfectly on Vercel
- ✅ Can view data in Supabase dashboard

---

**That's it! Add the environment variables and redeploy, and it will work!** 🎉

