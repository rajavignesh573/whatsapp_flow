# Fix: Supabase "proxy" Error

## The Error

```
Client.__init__() got an unexpected keyword argument 'proxy'
```

This is a **version compatibility issue** with the Supabase Python client.

## Solution

I've updated the code to:
1. ✅ Fix duplicate imports
2. ✅ Use simpler client initialization
3. ✅ Better error handling

## Next Steps

### 1. Commit and Push

```bash
cd /home/hp/whatsapp_flow
git add app.py requirements.txt
git commit -m "Fix Supabase client initialization error"
git push
```

### 2. Wait for Vercel to Redeploy

Vercel will automatically redeploy (takes 1-2 minutes).

### 3. Check Debug Endpoint

```bash
curl https://whatsapp-flow-pi.vercel.app/debug
```

**Should show:**
- `"supabase_configured": true` (if tables exist)
- OR `"init_error": "Tables don't exist..."` (if tables missing)

### 4. If Tables Don't Exist

Run the SQL script in Supabase:
1. Go to: https://supabase.com/dashboard/project/huyzlryubollexkuykgd/sql/new
2. Copy contents of `supabase_setup.sql`
3. Paste and run

### 5. Test Save User

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

## What Changed

1. **Removed duplicate import** - was importing `create_client` twice
2. **Simplified initialization** - no extra parameters
3. **Better error messages** - shows if tables are missing

## Expected Result

After redeploy:
- ✅ No more "proxy" error
- ✅ Supabase client initializes
- ✅ Save-user works (if tables exist)

