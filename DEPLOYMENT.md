# Deployment Guide

This guide provides instructions for deploying the Weather Intelligence Backend API.

## Local Development Setup

### Prerequisites
- Python 3.11+
- pip or conda
- Git

### Installation Steps

1. **Clone the repository:**
```bash
git clone https://github.com/Ragnork018/weather-intelligence-backend.git
cd weather-intelligence-backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
```
Edit `.env` and add your API keys:
```
OPENWEATHER_API_KEY=your_api_key
YOUTUBE_API_KEY=your_api_key
DATABASE_URL=sqlite:///./weather.db
DEBUG=True
```

5. **Run the application:**
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

## Docker Deployment

### Build Docker Image
```bash
docker build -t weather-intelligence-backend:latest .
```

### Run Docker Container
```bash
docker run -d \
  --name weather-api \
  -p 8000:8000 \
  -e OPENWEATHER_API_KEY=your_api_key \
  -e YOUTUBE_API_KEY=your_api_key \
  -e DATABASE_URL=postgresql://user:pass@db:5432/weather \
  weather-intelligence-backend:latest
```

## Cloud Deployment Options

### Option 1: Heroku

1. **Install Heroku CLI:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login and create app:**
```bash
heroku login
heroku create weather-intelligence-backend
```

3. **Add buildpack:**
```bash
heroku buildpacks:add heroku/python
```

4. **Set environment variables:**
```bash
heroku config:set OPENWEATHER_API_KEY=your_api_key
heroku config:set YOUTUBE_API_KEY=your_api_key
```

5. **Create Procfile in root:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

6. **Deploy:**
```bash
git push heroku main
```

### Option 2: Render

1. **Create account at render.com**

2. **Connect GitHub repository**

3. **Create new Web Service:**
   - Select repository
   - Set runtime to Python 3.11
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

4. **Add environment variables in dashboard**

5. **Deploy**

### Option 3: Railway

1. **Create account at railway.app**

2. **Install Railway CLI:**
```bash
npm i -g @railway/cli
```

3. **Initialize Railway project:**
```bash
railway init
railway up
```

4. **Set variables:**
```bash
railway variables
```

## Database Setup

### SQLite (Development)
```python
DATABASE_URL="sqlite:///./weather.db"
```

### PostgreSQL (Production)
```python
DATABASE_URL="postgresql://user:password@localhost:5432/weather_db"
```

Create database:
```bash
psql -U user -c "CREATE DATABASE weather_db;"
```

## API Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Interactive Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Monitoring & Logs

### Local logs
```bash
cat app.log
```

### Heroku logs
```bash
heroku logs --tail
```

### Render logs
View in dashboard

## Troubleshooting

### Common Issues

1. **Database connection error:**
   - Check DATABASE_URL format
   - Ensure database service is running

2. **API key errors:**
   - Verify OPENWEATHER_API_KEY and YOUTUBE_API_KEY are set
   - Check API key expiration

3. **Port already in use:**
```bash
lsof -i :8000  # Check what's using port
kill -9 <PID>  # Kill the process
```

## Production Best Practices

1. Always use environment variables for sensitive data
2. Enable HTTPS/TLS
3. Set up database backups
4. Monitor API performance
5. Implement rate limiting
6. Use gunicorn in production:
```bash
gunicorn app.main:app -w 4 -b 0.0.0.0:8000
```

## Scaling

1. Use gunicorn with multiple workers
2. Implement caching (Redis)
3. Use load balancer (nginx)
4. Separate database server

## Support

For issues or questions, visit:
https://github.com/Ragnork018/weather-intelligence-backend/issues

## Enhanced Cloud Deployment Guides

This section provides detailed step-by-step instructions for deploying to major cloud platforms.

### Heroku Deployment - Complete Guide

#### Prerequisites:
- GitHub account connected to Heroku
- Heroku account (free tier available)
- Heroku CLI installed

#### Step-by-Step Instructions:

1. **Install Heroku CLI and authenticate:**
```bash
# Install Heroku CLI (macOS)
brew tap heroku/brew && brew install heroku

# Login to Heroku
heroku login
```

2. **Create a Procfile in the project root:**
```bash
# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile
```

3. **Create Heroku app:**
```bash
# Create app (use unique name)
heroku create weather-intelligence-backend-<your-name>

# Or use automatic naming
heroku create
```

4. **Add Python buildpack:**
```bash
heroku buildpacks:add heroku/python
```

5. **Set environment variables:**
```bash
heroku config:set OPENWEATHER_API_KEY=your_actual_key
heroku config:set YOUTUBE_API_KEY=your_actual_key
heroku config:set DEBUG=False
```

6. **Configure database (PostgreSQL addon):**
```bash
# Add PostgreSQL addon (free tier: hobby-dev)
heroku addons:create heroku-postgresql:hobby-dev

# Verify database URL is set
heroku config | grep DATABASE_URL
```

7. **Deploy application:**
```bash
# Initialize git repo if not already done
git init
git add .
git commit -m "Initial deployment"

# Add Heroku remote
heroku git:remote -a weather-intelligence-backend-<your-name>

# Push to Heroku
git push heroku main
```

8. **Verify deployment:**
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# Open app in browser
heroku open
```

#### Heroku Useful Commands:
```bash
# Scale dynos
heroku ps:scale web=1

# View config
heroku config

# Connect to database
heroku pg:psql

# Check app info
heroku apps:info

# View application logs
heroku logs -n 50  # Last 50 lines
heroku logs --tail  # Real-time logs
```

#### Cost Estimation:
- Free tier: Limited dyno hours (1000/month)
- Paid tier: Starts at $7/month (standard-1x dyno)
- PostgreSQL: Free tier (hobby-dev) → $9/month (standard-0)

---

### Render Deployment - Complete Guide

#### Prerequisites:
- GitHub account
- Render account (render.com)
- Free tier available

#### Step-by-Step Instructions:

1. **Sign up and connect GitHub:**
   - Visit https://render.com
   - Click "Sign up with GitHub"
   - Authorize Render access to GitHub

2. **Create a new Web Service:**
   - Click "New +" → "Web Service"
   - Select your repository
   - Choose branch (main)

3. **Configure deployment settings:**
   - **Name:** weather-intelligence-backend
   - **Runtime:** Python 3.11
   - **Root Directory:** / (leave empty)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 8000`

4. **Add environment variables:**
   - Go to "Environment" section
   - Add key-value pairs:
     - `OPENWEATHER_API_KEY`: your_api_key
     - `YOUTUBE_API_KEY`: your_api_key
     - `DEBUG`: False
     - `DATABASE_URL`: postgresql://... (from PostgreSQL addon)

5. **Configure PostgreSQL database:**
   - Click "New +" → "PostgreSQL"
   - **Name:** weather-db
   - **Database:** weather
   - **User:** postgres
   - Copy the connection string
   - Add to Web Service environment variables

6. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically deploy
   - Monitor build progress in the logs

7. **Verify deployment:**
   - Wait for "Live" status
   - Click the generated URL
   - Check API docs at `/docs`

#### Render Useful Features:
```bash
# View logs in dashboard (automatic)
# Restart service: Manual trigger in dashboard
# Update environment: Change variables in dashboard
# Auto-deploy: Enabled for main branch by default
```

#### Cost Estimation:
- Web Service: Free tier (limited hours) → $7/month (Starter)
- PostgreSQL: Free tier → $15/month (Starter)
- Total starting cost: ~$22/month

---

### Railway Deployment - Complete Guide

#### Prerequisites:
- GitHub account
- Railway account (railway.app)
- Railway CLI installed

#### Step-by-Step Instructions:

1. **Sign up and install Railway CLI:**
```bash
# Sign up at https://railway.app
# Install Railway CLI
npm install -g @railway/cli

# Or using Homebrew (macOS)
brew install railway
```

2. **Login to Railway:**
```bash
railway login
```

3. **Initialize Railway project:**
```bash
# Create new project
railway init

# Follow prompts to link GitHub repository
```

4. **Create services:**
```bash
# Add database (PostgreSQL)
railway run psql
# Or add via dashboard
```

5. **Configure environment variables:**
```bash
railway variables
# Or set via CLI:
railway variables set OPENWEATHER_API_KEY=your_key
railway variables set YOUTUBE_API_KEY=your_key
railway variables set DEBUG=False
```

6. **Create railway.json configuration (optional):**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "dockerfile",
    "dockerfile": "Dockerfile"
  },
  "deploy": {
    "numReplicas": 1,
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port 8000"
  }
}
```

7. **Deploy application:**
```bash
railway up
```

8. **Verify deployment:**
```bash
# View logs
railway logs

# Check status
railway status

# Open in browser
railway open
```

#### Railway Useful Commands:
```bash
# View all services
railway services

# Connect to database
railway connect

# View environment
railway variables

# Redeploy
railway up

# View service logs
railway logs -s <service_name>
```

#### Cost Estimation:
- Pay as you go: ~$5-10/month for small apps
- Generous free tier with $5 credit monthly
- No minimum charges
- PostgreSQL: Included in usage

---

## Platform Comparison

| Feature | Heroku | Render | Railway |
|---------|--------|--------|----------|
| Free Tier | Limited dyno hours | Free tier available | $5 monthly credit |
| Setup Time | 10 mins | 5 mins | 10 mins |
| Auto-deploy | Yes (GitHub) | Yes (GitHub) | Yes (GitHub) |
| Database | Paid addon | Free tier | Included |
| Scaling | Easy | Easy | Easy |
| Custom Domain | Yes | Yes | Yes |
| SSL/HTTPS | Free | Free | Free |
| Regional Servers | Multiple | Multiple | Multiple |

---

## Recommended Deployment Checklist

Before going to production, verify:

- [ ] `.env` file is NOT committed to git
- [ ] All API keys are set in cloud platform environment
- [ ] Database connection is working
- [ ] DEBUG is set to False
- [ ] CORS_ORIGINS is properly configured
- [ ] Health check endpoint returns 200
- [ ] API documentation is accessible at `/docs`
- [ ] All external API calls are working
- [ ] Logs are being captured
- [ ] Monitoring/alerts are configured

---

## Monitoring and Maintenance

### Health Monitoring:
```bash
# Check API health
curl https://your-deployed-app.com/health

# Expected response:
# {"status": "healthy", "version": "0.1.0", "message": "API is operational"}
```

### Common Deployment Issues:

1. **ModuleNotFoundError:**
   - Solution: Ensure requirements.txt is updated
   - Run: `pip freeze > requirements.txt`

2. **Database connection failed:**
   - Solution: Verify DATABASE_URL is correctly set
   - Check: `heroku config` or platform's env variables

3. **Port binding error:**
   - Solution: Use $PORT environment variable
   - Already configured in Procfile/start commands

4. **API keys not working:**
   - Solution: Regenerate keys and update in platform
   - Test locally first with `.env` file

---

## Next Steps After Deployment

1. **Set up CI/CD pipeline** for automated testing
2. **Configure monitoring** (Sentry, DataDog)
3. **Set up custom domain** (optional)
4. **Enable SSL/HTTPS** (usually automatic)
5. **Configure backups** for database
6. **Set up alerts** for errors/failures
7. **Document API** endpoints for clients

---
