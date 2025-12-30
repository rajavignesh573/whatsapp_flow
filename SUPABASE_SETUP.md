# Supabase Setup Guide

This guide will help you set up Supabase as your database instead of JSON files.

## Why Supabase?

- ✅ **Works on Vercel** - No read-only filesystem issues
- ✅ **Free Tier** - Generous free tier for development
- ✅ **PostgreSQL** - Powerful relational database
- ✅ **Real-time** - Optional real-time subscriptions
- ✅ **Easy Setup** - Simple API and dashboard

---

## Step 1: Create Supabase Project

1. Go to https://supabase.com
2. Sign up (free) or log in
3. Click "New Project"
4. Fill in:
   - **Name:** `whatsapp-flow` (or any name)
   - **Database Password:** (save this securely)
   - **Region:** Choose closest to you
5. Click "Create new project"
6. Wait 2-3 minutes for project to be ready

---

## Step 2: Get API Credentials

1. In your Supabase project dashboard
2. Go to **Settings** → **API**
3. Copy these values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key** (starts with `eyJ...`)

---

## Step 3: Create Database Tables

1. In Supabase dashboard, go to **SQL Editor**
2. Click "New query"
3. Copy and paste the contents of `supabase_setup.sql`
4. Click "Run" (or press Ctrl+Enter)
5. Verify tables were created:
   - Go to **Table Editor**
   - You should see `messages` and `users` tables

---

## Step 4: Configure Environment Variables

### For Local Development

Create a `.env` file in your project root:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
WHATSAPP_VERIFY_TOKEN=your_verify_token_here
```

### For Vercel Deployment

1. Go to your Vercel project dashboard
2. Go to **Settings** → **Environment Variables**
3. Add these variables:

| Name | Value |
|------|-------|
| `SUPABASE_URL` | `https://your-project.supabase.co` |
| `SUPABASE_KEY` | `your-anon-key-here` |
| `WHATSAPP_VERIFY_TOKEN` | `your_verify_token_here` (optional) |

4. Click "Save"
5. Redeploy your application

---

## Step 5: Update Your Code

Replace `app.py` with `app_supabase.py`:

```bash
# Backup old app.py
mv app.py app_json_backup.py

# Use Supabase version
mv app_supabase.py app.py
```

Or manually copy the content from `app_supabase.py` to `app.py`.

---

## Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `supabase==2.3.4`
- `python-dotenv==1.0.0`

---

## Step 7: Test Locally

1. Make sure `.env` file is configured
2. Run the app:
   ```bash
   source venv/bin/activate
   python3 app.py
   ```
3. Test the endpoints:
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

## Step 8: Deploy to Vercel

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Migrate to Supabase"
   git push
   ```

2. Vercel will auto-deploy

3. Add environment variables in Vercel dashboard (if not done)

4. Test your deployed API:
   ```bash
   curl -X POST https://your-app.vercel.app/save-user \
     -H "Content-Type: application/json" \
     -d '{
       "user": "+1234567890",
       "parent_name": "John",
       "child_name": "Sarah",
       "wishlist": []
     }'
   ```

---

## Database Schema

### Messages Table
```sql
- id (BIGSERIAL PRIMARY KEY)
- data (JSONB) - Stores message data
- timestamp (TIMESTAMPTZ)
- created_at (TIMESTAMPTZ)
```

### Users Table
```sql
- id (BIGSERIAL PRIMARY KEY)
- phone (VARCHAR, UNIQUE) - User's phone number
- parent_name (VARCHAR)
- child_name (VARCHAR)
- wishlist (JSONB) - Array of wishlist items
- created_at (TIMESTAMPTZ)
- updated_at (TIMESTAMPTZ)
```

---

## Fallback to JSON

If Supabase is not configured, the app will automatically fall back to JSON files for local development. This is useful for:
- Testing without Supabase
- Local development
- Quick prototyping

To use JSON fallback:
- Don't set `SUPABASE_URL` and `SUPABASE_KEY` environment variables
- The app will use JSON files automatically

---

## Troubleshooting

### Error: "Supabase not configured"
- Check that `SUPABASE_URL` and `SUPABASE_KEY` are set
- Verify the values are correct (no extra spaces)
- Check `.env` file exists (for local) or Vercel env vars (for production)

### Error: "relation does not exist"
- Run the SQL setup script in Supabase SQL Editor
- Verify tables were created in Table Editor

### Error: "permission denied"
- Check that you're using the `anon/public` key (not the service role key)
- Verify RLS policies if Row Level Security is enabled

### Data not saving
- Check Supabase dashboard → Table Editor to see if data is there
- Check Vercel logs for errors
- Verify environment variables are set correctly

---

## Benefits of Supabase

1. **Works on Vercel** - No filesystem issues
2. **Scalable** - Handles growth easily
3. **Queryable** - Use SQL to query data
4. **Real-time** - Optional real-time features
5. **Dashboard** - Visual data management
6. **Backups** - Automatic backups included

---

## Next Steps

- ✅ Set up Supabase project
- ✅ Run SQL setup script
- ✅ Configure environment variables
- ✅ Update code to use Supabase
- ✅ Test locally
- ✅ Deploy to Vercel
- ✅ Test deployed API

Your API will now work perfectly on Vercel! 🎉

