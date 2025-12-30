# Quick Migration Guide: JSON to Supabase

## Quick Steps

1. **Create Supabase Project** (5 min)
   - Go to https://supabase.com
   - Create new project
   - Get URL and API key

2. **Run SQL Setup** (1 min)
   - Copy `supabase_setup.sql`
   - Paste in Supabase SQL Editor
   - Run it

3. **Set Environment Variables** (2 min)
   - Local: Create `.env` file
   - Vercel: Add in dashboard

4. **Switch Code** (1 min)
   ```bash
   mv app.py app_json_backup.py
   mv app_supabase.py app.py
   ```

5. **Install & Deploy** (2 min)
   ```bash
   pip install -r requirements.txt
   git add .
   git commit -m "Migrate to Supabase"
   git push
   ```

**Total time: ~10 minutes**

---

## Environment Variables

### Local (.env file)
```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Vercel
Add in Settings → Environment Variables:
- `SUPABASE_URL`
- `SUPABASE_KEY`

---

## Benefits

✅ Works on Vercel (no filesystem issues)  
✅ Free tier available  
✅ Scalable database  
✅ Visual dashboard  
✅ Automatic backups  

See `SUPABASE_SETUP.md` for detailed instructions.

