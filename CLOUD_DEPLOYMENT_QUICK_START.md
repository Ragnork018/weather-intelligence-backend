# Cloud Deployment Quick Start Guide

Choose your preferred cloud platform and follow the quick start steps below.

## ⚡ 5-Minute Quick Start

### Heroku (Easiest for First-Time Users)

```bash
# 1. Install Heroku CLI and login
brew tap heroku/brew && brew install heroku
heroku login

# 2. Clone and navigate to project
git clone https://github.com/Ragnork018/weather-intelligence-backend.git
cd weather-intelligence-backend

# 3. Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 4. Create app and deploy
heroku create
heroku config:set OPENWEATHER_API_KEY=your_key
heroku config:set YOUTUBE_API_KEY=your_key
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main

# 5. Check deployment
heroku logs --tail
heroku open
```

**Cost:** Free tier available (limited dyno hours) → $7+/month paid

---

### Render (Best Free Tier)

```bash
# 1. Create account at render.com and connect GitHub
# (No CLI needed - all done in dashboard)

# 2. Click "New +" → "Web Service"
# 3. Select your repository and branch (main)
# 4. Set these values:
#    - Runtime: Python 3.11
#    - Build: pip install -r requirements.txt
#    - Start: uvicorn app.main:app --host 0.0.0.0 --port 8000

# 5. Add Environment Variables:
#    - OPENWEATHER_API_KEY=your_key
#    - YOUTUBE_API_KEY=your_key
#    - DEBUG=False

# 6. Add PostgreSQL:
#    Click "New +" → "PostgreSQL" and link to web service

# 7. Deploy (automatic on main branch push)
```

**Cost:** Free tier available (up to 750 hours/month)

---

### Railway (Most Affordable)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli
# or brew install railway

# 2. Clone and navigate
git clone https://github.com/Ragnork018/weather-intelligence-backend.git
cd weather-intelligence-backend

# 3. Initialize project
railway init
railway up

# 4. Set environment variables
railway variables set OPENWEATHER_API_KEY=your_key
railway variables set YOUTUBE_API_KEY=your_key

# 5. View deployment
railway logs
railway open
```

**Cost:** ~$5-10/month (pay-as-you-go, $5 monthly credit)

---

## 📊 Platform Comparison

| Feature | Heroku | Render | Railway |
|---------|--------|--------|----------|
| Setup Time | 10 min | 5 min | 10 min |
| Free Tier | ✓ Limited | ✓ Generous | ✓ $5 Credit |
| Database | ✓ Paid | ✓ Free tier | ✓ Included |
| Auto-deploy | ✓ GitHub | ✓ GitHub | ✓ GitHub |
| CLI Required | ✓ Yes | ✗ No | ✓ Yes |
| Ease of Use | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🔑 Required API Keys

Before deploying, get these free API keys:

### 1. OpenWeatherMap API Key
- Visit: https://openweathermap.org/api
- Sign up for free account
- Generate API key from dashboard

### 2. YouTube API Key
- Visit: https://console.cloud.google.com/
- Create new project
- Enable YouTube Data API v3
- Create API key from credentials

---

## ✅ Deployment Checklist

Before deploying, verify:

- [ ] API keys are generated and ready
- [ ] Repository is pushed to GitHub
- [ ] `.env` file is in `.gitignore` (not committed)
- [ ] requirements.txt is up to date
- [ ] Dockerfile exists (for some platforms)
- [ ] DEBUG is set to False in production

---

## 🔗 After Deployment

### Access Your API
- **Root:** `https://your-app-url.com/`
- **Docs:** `https://your-app-url.com/docs`
- **Health:** `https://your-app-url.com/health`
- **ReDoc:** `https://your-app-url.com/redoc`

### Test Health Check
```bash
curl https://your-app-url.com/health
# Expected: {"status": "healthy", "version": "0.1.0", ...}
```

---

## 🆘 Common Issues

### ModuleNotFoundError
**Solution:** Update requirements.txt
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
```

### Database Connection Failed
**Solution:** Verify DATABASE_URL is set correctly
```bash
# Heroku
heroku config | grep DATABASE_URL

# Render/Railway: Check dashboard environment variables
```

### Port Binding Error
**Solution:** Already handled in our code. The start commands use `$PORT` variable.

### API Keys Not Working
**Solution:** Verify keys are correctly set
```bash
# Test locally first with .env file
source venv/bin/activate
python -m uvicorn app.main:app --reload
```

---

## 📚 Detailed Guides

For step-by-step instructions with screenshots, see:
- [Full DEPLOYMENT.md](./DEPLOYMENT.md) - Comprehensive guide for all deployment methods

---

## 🚀 Next Steps

1. **Choose your platform** based on the comparison table above
2. **Get your API keys** from OpenWeatherMap and Google Cloud
3. **Follow the quick start** for your chosen platform
4. **Test your deployment** using the health check endpoint
5. **Share your API** with others or integrate into frontend

---

## ⚙️ Recommended Setup

For best experience, we recommend:
- **Beginners:** Render (easiest, free tier is generous)
- **Budget-conscious:** Railway (most affordable long-term)
- **Established users:** Heroku (mature ecosystem, more features)

---

Have questions? Check [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed troubleshooting and advanced configurations.
