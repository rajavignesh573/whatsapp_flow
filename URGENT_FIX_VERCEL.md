# ⚠️ URGENT: Fix Vercel Environment Variables

## Current Status

Your health check shows:
```json
{
  "supabase_configured": false,
  "database": "JSON Files"
}
```

**This means Vercel doesn't have the Supabase environment variables!**

---

## 🔧 Fix Steps (5 Minutes)

### Step 1: Open Vercel Dashboard

1. Go to: https://vercel.com/dashboard
2. Find and click on your project: `whatsapp-flow` (or `whatsapp-flow-pi`)

### Step 2: Go to Environment Variables

1. Click **Settings** (in the top menu)
2. Click **Environment Variables** (in the left sidebar)

### Step 3: Add SUPABASE_URL

1. Click the **"Add New"** button
2. Fill in:
   - **Key:** `SUPABASE_URL`
   - **Value:** `https://huyzlryubollexkuykgd.supabase.co`
   - **Environment:** Check all three boxes:
     - ☑ Production
     - ☑ Preview  
     - ☑ Development
3. Click **Save**

### Step 4: Add SUPABASE_KEY

1. Click **"Add New"** button again
2. Fill in:
   - **Key:** `SUPABASE_KEY`
   - **Value:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh1eXpscnl1Ym9sbGV4a3V5a2dkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcwOTE2NTUsImV4cCI6MjA4MjY2NzY1NX0.709TKB1MZbLXLb210KSe4nj4cHhgwK9jDZWhdFOL6fY`
   - **Environment:** Check all three boxes:
     - ☑ Production
     - ☑ Preview
     - ☑ Development
3. Click **Save**

### Step 5: Redeploy (CRITICAL!)

**You MUST redeploy for the variables to take effect!**

**Option A: Redeploy from Dashboard**
1. Go to **Deployments** tab
2. Find the latest deployment
3. Click the **three dots** (⋯) menu
4. Click **Redeploy**
5. Wait 1-2 minutes

**Option B: Push a Commit**
```bash
cd /home/hp/whatsapp_flow
git commit --allow-empty -m "Trigger redeploy for Supabase"
git push
```

---

## ✅ Verify It's Fixed

### Test 1: Health Check

```bash
curl https://whatsapp-flow-pi.vercel.app/health
```

**Should show:**
```json
{
  "status": "healthy",
  "database": "Supabase",
  "supabase_configured": true
}
```

✅ If you see `"supabase_configured": true`, it's working!

### Test 2: Save User

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

**Should return:**
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

✅ No more "read-only file system" error!

---

## 🚨 Common Mistakes

### ❌ Wrong: Only adding to Production
- Must add to **all environments** (Production, Preview, Development)

### ❌ Wrong: Not redeploying
- Environment variables only take effect after redeploy

### ❌ Wrong: Typo in variable name
- Must be exactly: `SUPABASE_URL` and `SUPABASE_KEY` (case-sensitive)

### ❌ Wrong: Missing https:// in URL
- Must be: `https://huyzlryubollexkuykgd.supabase.co`

---

## 📋 Quick Checklist

- [ ] Added `SUPABASE_URL` to Vercel
- [ ] Added `SUPABASE_KEY` to Vercel
- [ ] Selected all 3 environments (Production, Preview, Development)
- [ ] Clicked "Save" for both variables
- [ ] Redeployed the application
- [ ] Health check shows `supabase_configured: true`
- [ ] Save-user endpoint works without errors

---

## 🎯 After Fix

Once you've:
1. ✅ Added both environment variables
2. ✅ Redeployed

Your Kapso webhook will work perfectly! The error will be gone.

---

## Still Not Working?

If after redeploy you still see `supabase_configured: false`:

1. **Check Vercel Logs:**
   - Go to Deployments → Latest → View Function Logs
   - Look for Supabase initialization errors

2. **Verify Supabase Tables:**
   - Make sure you ran the SQL setup script
   - Go to: https://supabase.com/dashboard/project/huyzlryubollexkuykgd/editor
   - Should see `messages` and `users` tables

3. **Double-check Environment Variables:**
   - Go to Settings → Environment Variables
   - Verify both are there and spelled correctly

---

**Do this now and your API will work!** 🚀

