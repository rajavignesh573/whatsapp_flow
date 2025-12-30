# Vercel Environment Variables Setup

## Add These to Vercel

Go to your Vercel project dashboard → **Settings** → **Environment Variables**

Add these two variables:

### 1. SUPABASE_URL
```
Name: SUPABASE_URL
Value: https://huyzlryubollexkuykgd.supabase.co
Environment: Production, Preview, Development
```

### 2. SUPABASE_KEY
```
Name: SUPABASE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh1eXpscnl1Ym9sbGV4a3V5a2dkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcwOTE2NTUsImV4cCI6MjA4MjY2NzY1NX0.709TKB1MZbLXLb210KSe4nj4cHhgwK9jDZWhdFOL6fY
Environment: Production, Preview, Development
```

## After Adding Variables

1. Click **Save**
2. Go to **Deployments** tab
3. Click **Redeploy** on the latest deployment
4. Or push a new commit to trigger auto-deploy

## Verify It Works

After redeploy, test:
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

## Test Save User

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

This should now work on Vercel! 🎉

