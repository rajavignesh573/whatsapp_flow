# Quick Deploy Guide - 5 Minutes ⚡

## Fastest Way: Vercel (Recommended) 🚀

**Why Vercel?**
- ✅ Deploys in 1-2 minutes
- ✅ 100% free for personal projects
- ✅ Global CDN (fast worldwide)
- ✅ Automatic HTTPS
- ✅ Zero configuration

### Step 1: Push to GitHub (2 minutes)

```bash
# Initialize git (if not done)
git init
git add .
git commit -m "WhatsApp Flow API"

# Create repo on GitHub.com, then:
git remote add origin https://github.com/YOUR_USERNAME/whatsapp_flow.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Vercel (1 minute)

1. Go to https://vercel.com
2. Sign up with GitHub (one click)
3. Click "Add New..." → "Project"
4. Import your GitHub repo
5. Click "Deploy" (auto-detects everything!)
6. Wait 1-2 minutes

### Step 3: Get Your URL

Your API will be live at:
```
https://your-project-name.vercel.app
```

### Step 4: Test It

```bash
# Health check
curl https://your-project-name.vercel.app/health

# Test webhook
curl -X POST https://your-project-name.vercel.app/check-or-create-user \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890"}'
```

---

## Alternative: Render.com (Also Easy)

**Free Tier:** 750 hours/month (enough for 24/7)

### Steps:

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
6. Click "Create Web Service"
7. Wait 2-3 minutes

Your API: `https://your-app-name.onrender.com`

---

## Alternative: Railway.app (Even Faster)

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Railway auto-detects everything!
6. Done! Get your URL from dashboard

---

## Alternative: Replit (No Git Needed)

1. Go to https://replit.com
2. Sign up (free)
3. Create new Python Repl
4. Copy-paste all your files
5. Click "Run"
6. Get instant public URL!

---

## Use in Kapso

Once deployed, use your cloud URL:

**In Kapso Webhook Step:**
```
URL: https://your-app.vercel.app/check-or-create-user
Method: POST
Body: {"phone": "{{context.phone_number}}"}
```

**For Save User:**
```
URL: https://your-app.vercel.app/save-user
Method: POST
Body: {
  "user": "{{context.phone_number}}",
  "parent_name": "{{parent_name}}",
  "child_name": "{{child_name}}",
  "wishlist": []
}
```

---

## That's It! 🎉

Your API is now live on the internet and ready to use with Kapso!

**Recommended:** Start with **Vercel** - it's the fastest and easiest! ⚡
