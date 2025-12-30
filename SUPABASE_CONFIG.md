# Your Supabase Configuration

## Project Details

**Project ID:** `huyzlryubollexkuykgd`  
**Project URL:** `https://huyzlryubollexkuykgd.supabase.co`  
**Dashboard:** https://supabase.com/dashboard/project/huyzlryubollexkuykgd/settings/general

---

## Step 1: Get Your API Key

1. Go to: https://supabase.com/dashboard/project/huyzlryubollexkuykgd/settings/api
2. Under **Project API keys**, find:
   - **Project URL:** `https://huyzlryubollexkuykgd.supabase.co`
   - **anon public key:** (starts with `eyJ...`) - Copy this!

---

## Step 2: Set Environment Variables

### For Local Development

Create `.env` file in your project root:

```bash
SUPABASE_URL=https://huyzlryubollexkuykgd.supabase.co
SUPABASE_KEY=your-anon-public-key-here
WHATSAPP_VERIFY_TOKEN=your_verify_token_here
```

Replace `your-anon-public-key-here` with the key from Step 1.

### For Vercel

1. Go to your Vercel project dashboard
2. Settings → Environment Variables
3. Add:

| Name | Value |
|------|-------|
| `SUPABASE_URL` | `https://huyzlryubollexkuykgd.supabase.co` |
| `SUPABASE_KEY` | `your-anon-public-key-here` |

---

## Step 3: Run SQL Setup

1. Go to: https://supabase.com/dashboard/project/huyzlryubollexkuykgd/sql/new
2. Copy the contents of `supabase_setup.sql`
3. Paste and click "Run"
4. Verify tables were created in Table Editor

---

## Step 4: Switch to Supabase Version

```bash
cd /home/hp/whatsapp_flow

# Backup current app
mv app.py app_json_backup.py

# Use Supabase version
mv app_supabase.py app.py
```

---

## Step 5: Install Dependencies

```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## Step 6: Test Locally

```bash
python3 app.py
```

Test the endpoint:
```bash
curl -X POST http://localhost:5000/save-user \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": []
  }'
```

---

## Step 7: Deploy to Vercel

1. Commit changes:
   ```bash
   git add .
   git commit -m "Configure Supabase integration"
   git push
   ```

2. Add environment variables in Vercel (if not done)

3. Vercel will auto-deploy

4. Test deployed API:
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

## Quick Links

- **API Settings:** https://supabase.com/dashboard/project/huyzlryubollexkuykgd/settings/api
- **SQL Editor:** https://supabase.com/dashboard/project/huyzlryubollexkuykgd/sql/new
- **Table Editor:** https://supabase.com/dashboard/project/huyzlryubollexkuykgd/editor
- **Project Settings:** https://supabase.com/dashboard/project/huyzlryubollexkuykgd/settings/general

---

## Your Supabase URL Format

Your API URL is: `https://huyzlryubollexkuykgd.supabase.co`

Use this in your `.env` file and Vercel environment variables.

