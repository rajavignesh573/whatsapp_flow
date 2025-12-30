# Quick Supabase Setup - Your Project

## Your Project Details

**Project ID:** `huyzlryubollexkuykgd`  
**Supabase URL:** `https://huyzlryubollexkuykgd.supabase.co`

---

## 🚀 Quick Setup (5 Steps)

### Step 1: Get API Key (1 min)

1. Go to: https://supabase.com/dashboard/project/huyzlryubollexkuykgd/settings/api
2. Under **Project API keys** → **anon public**
3. Click **Copy** to copy the key (starts with `eyJ...`)

---

### Step 2: Create Database Tables (1 min)

1. Go to: https://supabase.com/dashboard/project/huyzlryubollexkuykgd/sql/new
2. Copy the entire contents of `supabase_setup.sql`
3. Paste in the SQL editor
4. Click **Run** (or press Ctrl+Enter)
5. You should see "Success. No rows returned"

---

### Step 3: Create .env File (1 min)

Create `.env` file in your project:

```bash
cd /home/hp/whatsapp_flow
cat > .env << 'EOF'
SUPABASE_URL=https://huyzlryubollexkuykgd.supabase.co
SUPABASE_KEY=paste-your-anon-key-here
WHATSAPP_VERIFY_TOKEN=your_verify_token_here
EOF
```

Replace `paste-your-anon-key-here` with the key from Step 1.

---

### Step 4: Switch to Supabase Version (1 min)

```bash
cd /home/hp/whatsapp_flow

# Backup current version
mv app.py app_json_backup.py

# Use Supabase version
mv app_supabase.py app.py
```

---

### Step 5: Install & Test (1 min)

```bash
# Install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Test locally
python3 app.py
```

In another terminal:
```bash
curl -X POST http://localhost:5000/health
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

---

## 📦 Deploy to Vercel

### Add Environment Variables in Vercel

1. Go to your Vercel project dashboard
2. **Settings** → **Environment Variables**
3. Add:

| Name | Value |
|------|-------|
| `SUPABASE_URL` | `https://huyzlryubollexkuykgd.supabase.co` |
| `SUPABASE_KEY` | `your-anon-public-key-here` |

4. Click **Save**
5. Redeploy (or push new commit)

---

## ✅ Verify Setup

### Check Tables Were Created

1. Go to: https://supabase.com/dashboard/project/huyzlryubollexkuykgd/editor
2. You should see:
   - `messages` table
   - `users` table

### Test API

```bash
# Test save user
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

1. Go to: https://supabase.com/dashboard/project/huyzlryubollexkuykgd/editor
2. Click on `users` table
3. You should see your test data!

---

## 🔗 Quick Links

- **API Settings:** https://supabase.com/dashboard/project/huyzlryubollexkuykgd/settings/api
- **SQL Editor:** https://supabase.com/dashboard/project/huyzlryubollexkuykgd/sql/new
- **Table Editor:** https://supabase.com/dashboard/project/huyzlryubollexkuykgd/editor
- **Project Settings:** https://supabase.com/dashboard/project/huyzlryubollexkuykgd/settings/general

---

## 🎉 Done!

Your API now uses Supabase and will work perfectly on Vercel!

