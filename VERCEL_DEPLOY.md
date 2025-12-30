# Deploy to Vercel - Free & Easy 🚀

Vercel is excellent for serverless Flask apps with automatic HTTPS, global CDN, and zero configuration.

## Why Vercel?

- ✅ **100% Free** for personal projects
- ✅ **Automatic HTTPS** and custom domains
- ✅ **Global CDN** - Fast worldwide
- ✅ **Zero Configuration** - Just push to GitHub
- ✅ **Instant Deploys** - Deploys in seconds
- ✅ **Serverless** - Scales automatically

## Quick Deploy (3 Steps)

### Step 1: Install Vercel CLI (Optional but Recommended)

```bash
npm install -g vercel
```

Or use the web interface (no CLI needed).

### Step 2: Deploy via Web Interface (Easiest)

1. **Push to GitHub** (if not done):
   ```bash
   git init
   git add .
   git commit -m "WhatsApp Flow API"
   git remote add origin https://github.com/YOUR_USERNAME/whatsapp_flow.git
   git push -u origin main
   ```

2. **Go to Vercel**: https://vercel.com
   - Sign up with GitHub (one click)

3. **Import Project**:
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Vercel auto-detects Python/Flask

4. **Configure** (usually auto-detected):
   - **Framework Preset:** Other
   - **Root Directory:** `./`
   - **Build Command:** (leave empty or `pip install -r requirements.txt`)
   - **Output Directory:** (leave empty)

5. **Environment Variables** (optional):
   - `WHATSAPP_VERIFY_TOKEN`: Your webhook verify token

6. **Deploy**: Click "Deploy"
   - Wait 1-2 minutes

7. **Get Your URL**: 
   - Your API will be at: `https://your-project-name.vercel.app`
   - Example: `https://whatsapp-flow-api.vercel.app`

### Step 3: Deploy via CLI (Alternative)

```bash
# Login to Vercel
vercel login

# Deploy (first time)
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No
# - Project name? whatsapp-flow-api
# - Directory? ./
# - Override settings? No

# For production
vercel --prod
```

## Your API URLs

After deployment, your endpoints will be:

- **Base URL**: `https://your-project.vercel.app`
- **Health Check**: `https://your-project.vercel.app/health`
- **Check User**: `https://your-project.vercel.app/check-or-create-user`
- **Save User**: `https://your-project.vercel.app/save-user`
- **Webhook**: `https://your-project.vercel.app/webhook`

## Test Your Deployed API

```bash
# Health check
curl https://your-project.vercel.app/health

# Check user
curl -X POST https://your-project.vercel.app/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'

# Save user
curl -X POST https://your-project.vercel.app/save-user \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": []
  }'
```

Or use the test script:
```bash
./test_deployed_api.sh https://your-project.vercel.app
```

## Use in Kapso

**Webhook Configuration:**
```
URL: https://your-project.vercel.app/check-or-create-user
Method: POST
Body: {"phone": "{{context.phone_number}}"}
```

**Save User:**
```
URL: https://your-project.vercel.app/save-user
Method: POST
Body: {
  "user": "{{context.phone_number}}",
  "parent_name": "{{parent_name}}",
  "child_name": "{{child_name}}",
  "wishlist": []
}
```

## Important Notes for Vercel

### 1. **File System Limitations**
   - Vercel uses serverless functions (read-only filesystem)
   - JSON files will work, but consider:
     - Using Vercel KV (Redis) for production
     - Using a database (MongoDB, PostgreSQL)
     - For testing, JSON files work fine

### 2. **Cold Starts**
   - First request may be slower (~1-2 seconds)
   - Subsequent requests are fast
   - Free tier has generous limits

### 3. **Function Timeout**
   - Free tier: 10 seconds per function
   - Pro tier: 60 seconds
   - Your API should be fine (fast responses)

### 4. **Automatic Deploys**
   - Every push to main branch = new deploy
   - Preview deployments for PRs
   - Zero downtime deployments

## Vercel vs Other Platforms

| Feature | Vercel | Render | Railway |
|---------|--------|--------|---------|
| Free Tier | ✅ Generous | ✅ 750hrs/month | ✅ $5 credit |
| Setup Time | 2 min | 5 min | 3 min |
| Global CDN | ✅ | ❌ | ❌ |
| Auto Deploy | ✅ | ✅ | ✅ |
| Serverless | ✅ | ❌ | ❌ |
| File Persistence | ⚠️ Limited | ✅ | ✅ |

## Troubleshooting

### Issue: "Module not found"
**Solution**: Make sure `requirements.txt` includes all dependencies

### Issue: "Function timeout"
**Solution**: Optimize your code or upgrade to Pro plan

### Issue: "File not persisting"
**Solution**: Use Vercel KV or external database for production

### Issue: "CORS errors"
**Solution**: Add CORS to your Flask app:
```python
from flask_cors import CORS
CORS(app)
```

## Upgrade to Production Database

For production, consider using:
- **Vercel KV** (Redis) - Built-in, easy
- **MongoDB Atlas** - Free tier available
- **Supabase** - PostgreSQL, free tier
- **PlanetScale** - MySQL, free tier

## That's It! 🎉

Your Flask API is now live on Vercel with:
- ✅ Free HTTPS
- ✅ Global CDN
- ✅ Automatic deployments
- ✅ Zero configuration

Deploy time: **~2 minutes** ⚡

