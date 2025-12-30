# Supabase Setup for Vercel - What You Need to Do

## ✅ Required: Create Database Tables

**This is the ONLY thing you MUST do in Supabase!**

### Step 1: Run SQL Setup Script

1. **Go to SQL Editor:**
   https://supabase.com/dashboard/project/huyzlryubollexkuykgd/sql/new

2. **Copy the SQL script:**
   - Open `supabase_setup.sql` from your project
   - Copy ALL the contents

3. **Paste and Run:**
   - Paste in Supabase SQL Editor
   - Click **Run** (or press Ctrl+Enter)
   - You should see: "Success. No rows returned"

4. **Verify Tables Created:**
   - Go to: https://supabase.com/dashboard/project/huyzlryubollexkuykgd/editor
   - You should see two tables:
     - ✅ `messages`
     - ✅ `users`

---

## ✅ That's It! No Other Configuration Needed

The **anon public key** you're using already has the right permissions to:
- ✅ Read data
- ✅ Insert data
- ✅ Update data
- ✅ Delete data (if needed)

**No Row Level Security (RLS) setup needed** - the anon key works by default for API access.

---

## 🔍 Verify Setup

### Check Tables Exist

1. Go to: https://supabase.com/dashboard/project/huyzlryubollexkuykgd/editor
2. You should see:
   - `messages` table (with columns: id, data, timestamp, created_at)
   - `users` table (with columns: id, phone, parent_name, child_name, wishlist, created_at, updated_at)

### Test After Vercel Deploy

Once you've:
1. ✅ Run the SQL script
2. ✅ Added environment variables to Vercel
3. ✅ Deployed to Vercel

Test it:
```bash
curl https://whatsapp-flow-pi.vercel.app/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "Supabase",
  "supabase_configured": true
}
```

Then test saving a user:
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

### Check Data in Supabase

After testing, check your data:
1. Go to: https://supabase.com/dashboard/project/huyzlryubollexkuykgd/editor
2. Click on `users` table
3. You should see the test data!

---

## 📋 Summary

**What you need to do in Supabase:**
1. ✅ Run the SQL setup script (create tables) - **REQUIRED**

**What you DON'T need to do:**
- ❌ No RLS policies needed
- ❌ No API key changes needed
- ❌ No authentication setup needed
- ❌ No other configuration needed

**What Vercel needs:**
- ✅ Environment variables (SUPABASE_URL and SUPABASE_KEY)
- ✅ That's it!

---

## 🚨 Common Issues

### "relation does not exist"
**Solution:** You haven't run the SQL setup script yet. Run it now!

### "permission denied"
**Solution:** Make sure you're using the **anon public** key (not service_role key)

### "connection refused"
**Solution:** Check that SUPABASE_URL is correct: `https://huyzlryubollexkuykgd.supabase.co`

---

## ✅ Checklist

- [ ] Run SQL setup script in Supabase
- [ ] Verify tables exist (messages and users)
- [ ] Add SUPABASE_URL to Vercel
- [ ] Add SUPABASE_KEY to Vercel
- [ ] Deploy to Vercel
- [ ] Test health endpoint
- [ ] Test save-user endpoint
- [ ] Verify data appears in Supabase dashboard

---

**That's all! Once you run the SQL script, Vercel can call Supabase without any other setup.** 🎉

