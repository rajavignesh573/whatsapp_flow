# Free Cloud Deployment Guide

This guide shows you how to deploy your WhatsApp API to free cloud platforms.

## Option 1: Vercel (Fastest & Serverless) ⚡ NEW

**Free Tier:** Generous limits, global CDN, automatic HTTPS

### Steps:

1. **Push to GitHub** (if not done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/whatsapp_flow.git
   git push -u origin main
   ```

2. **Go to Vercel**: https://vercel.com
   - Sign up with GitHub (one click)

3. **Import Project**:
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Vercel auto-detects Python/Flask

4. **Deploy**: Click "Deploy" (usually no config needed)
   - Wait 1-2 minutes

5. **Get Your URL**: 
   - Your API: `https://your-project.vercel.app`

**See `VERCEL_DEPLOY.md` for detailed instructions.**

---

## Option 2: Render.com (Easiest & Recommended) ⭐

**Free Tier:** 750 hours/month (enough for 24/7), free SSL, custom domain

### Steps:

1. **Create GitHub Repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/whatsapp_flow.git
   git push -u origin main
   ```

2. **Sign up at Render.com**: https://render.com (use GitHub to sign in)

3. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `whatsapp_flow` repository

4. **Configure Service**:
   - **Name:** `whatsapp-flow-api` (or any name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan:** Free

5. **Environment Variables** (optional):
   - `WHATSAPP_VERIFY_TOKEN`: Your webhook verify token

6. **Deploy**: Click "Create Web Service"

7. **Get Your URL**: 
   - Your API will be available at: `https://whatsapp-flow-api.onrender.com`
   - Use this URL in Kapso: `https://whatsapp-flow-api.onrender.com/check-or-create-user`

### Test Your Deployed API:
```bash
curl -X POST https://your-app-name.onrender.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "message"}'
```

---

## Option 2: Railway.app (Very Easy)

**Free Tier:** $5 credit/month (enough for small apps)

### Steps:

1. **Sign up**: https://railway.app (use GitHub)

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure**:
   - Railway auto-detects Python
   - It will use `requirements.txt` automatically
   - Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

4. **Deploy**: Railway will automatically deploy

5. **Get URL**: Railway provides a URL like `https://your-app.up.railway.app`

---

## Option 3: PythonAnywhere (Simple for Python)

**Free Tier:** Limited but good for testing

### Steps:

1. **Sign up**: https://www.pythonanywhere.com

2. **Upload Files**:
   - Go to "Files" tab
   - Upload all your files (app.py, requirements.txt, etc.)

3. **Open Bash Console**:
   - Install dependencies: `pip3.10 install --user flask gunicorn`

4. **Create Web App**:
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Flask"
   - Select Python 3.10
   - Enter path to your app.py

5. **Configure WSGI**:
   - Click on WSGI configuration file
   - Update it to point to your app

6. **Reload**: Click "Reload" button

7. **Get URL**: `https://YOUR_USERNAME.pythonanywhere.com`

---

## Option 4: Fly.io (Good Free Tier)

**Free Tier:** 3 shared-cpu VMs, 3GB persistent storage

### Steps:

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**:
   ```bash
   fly auth login
   ```

3. **Create App**:
   ```bash
   fly launch
   ```

4. **Deploy**:
   ```bash
   fly deploy
   ```

5. **Get URL**: Fly provides a URL automatically

---

## Option 5: Replit (Easiest for Quick Testing)

**Free Tier:** Always-on repls available

### Steps:

1. **Sign up**: https://replit.com

2. **Create Repl**:
   - Click "Create Repl"
   - Choose "Python"
   - Name it "whatsapp-flow-api"

3. **Upload Files**:
   - Copy all your files into the Repl

4. **Run**:
   - Click "Run" button
   - Replit provides a public URL automatically

---

## Quick Setup Script for Render.com

Create a `render.yaml` file for easier deployment:

```yaml
services:
  - type: web
    name: whatsapp-flow-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
    envVars:
      - key: WHATSAPP_VERIFY_TOKEN
        value: your_verify_token_here
```

---

## Testing Your Deployed API

Once deployed, test with:

```bash
# Health check
curl https://your-app-url.com/health

# Check user
curl -X POST https://your-app-url.com/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'

# Save user
curl -X POST https://your-app-url.com/save-user \
  -H "Content-Type: application/json" \
  -d '{
    "user": "+1234567890",
    "parent_name": "John",
    "child_name": "Sarah",
    "wishlist": []
  }'
```

---

## Important Notes

1. **JSON Database Persistence**: 
   - Render.com: Files persist between deployments
   - Railway: Use volumes for persistence
   - PythonAnywhere: Files persist
   - Fly.io: Use volumes for persistence

2. **Environment Variables**: 
   - Set `WHATSAPP_VERIFY_TOKEN` in your platform's environment settings

3. **HTTPS**: 
   - All platforms provide free SSL certificates
   - Use HTTPS URLs in Kapso webhook configuration

4. **CORS** (if needed): 
   - Add CORS support if calling from browser:
   ```python
   from flask_cors import CORS
   CORS(app)
   ```

---

## Recommended: Render.com

**Why Render.com?**
- ✅ Easiest setup
- ✅ Free tier is generous
- ✅ Auto-deploys from GitHub
- ✅ Free SSL
- ✅ Good documentation
- ✅ No credit card required

**Quick Start:**
1. Push code to GitHub
2. Connect GitHub to Render
3. Deploy
4. Done! 🎉

---

## Troubleshooting

**Port Issues**: Make sure your app uses `$PORT` environment variable:
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

**Database Files**: JSON files will persist on most platforms, but consider using a database for production.

**Logs**: Check platform logs if deployment fails.

