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
