# Weather Intelligence Backend

**Backend API for Weather Intelligence Application** - A professional-grade FastAPI backend for retrieving, storing, and exporting weather data with real-time API integrations.

**Built for:** PM Accelerator AI Engineer Internship Assessment (Tech Assessment #2 - Backend)

## 📋 Overview

This is a backend-first, production-ready FastAPI application that demonstrates:
- **Clean architecture** with layered design (API → Services → CRUD → DB)
- **Real-time API integrations** (OpenWeatherMap, YouTube)
- **Full CRUD operations** with SQLAlchemy ORM
- **Data persistence** with SQLite/PostgreSQL
- **Export functionality** to CSV and JSON formats
- **Robust error handling** and input validation
- **OpenAPI documentation** built-in

## 🎯 Key Features

✅ **Weather Data Retrieval**
- Accept location input (city, coordinates, landmarks, ZIP codes)
- Validate location existence via OpenWeatherMap API
- Fetch real-time weather data with comprehensive attributes

✅ **Database Persistence (CRUD)**
- CREATE: Store weather queries with dates and API responses
- READ: Retrieve historical requests with filtering
- UPDATE: Modify stored records with validation
- DELETE: Remove records from database

✅ **External API Integrations**
- OpenWeatherMap for weather data
- YouTube API for location-related videos
- Extensible design for additional APIs

✅ **Data Export**
- CSV export of all weather requests
- JSON export with full payload details

✅ **Production-Grade**
- Async/await for high concurrency
- Proper error handling with meaningful messages
- Input validation with Pydantic
- Scalable architecture ready for AI features

## 🏗️ Architecture

```
API Layer (routers/)
    ↓
Service Layer (services/)
    ↓
CRUD Layer (crud.py)
    ↓
Database Layer (models.py + database.py)
    ↓
External APIs (external/)
```

### Directory Structure

```
weather-intelligence-backend/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration & settings
│   ├── database.py            # SQLAlchemy setup
│   ├── models.py              # Database models
│   ├── schemas.py             # Pydantic schemas
│   ├── crud.py                # Database operations
│   ├── main.py                # FastAPI app initialization
│   ├── services/
│   │   ├── __init__.py
│   │   ├── weather_service.py # Business logic
│   │   └── export_service.py  # Data export logic
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── weather_requests.py # Weather endpoints
│   │   └── exports.py         # Export endpoints
│   ├── external/
│   │   ├── __init__.py
│   │   ├── weather_client.py  # OpenWeatherMap client
│   │   └── youtube_client.py  # YouTube API client
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py      # Custom exceptions
│       └── validators.py      # Validation helpers
├── requirements.txt
├── .env.example
├── .env
├── README.md
└── weather.db                 # SQLite database (auto-generated)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip
- OpenWeatherMap API key (free tier available at openweathermap.org)
- YouTube API key (optional, for location videos)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Ragnork018/weather-intelligence-backend.git
cd weather-intelligence-backend
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
OPENWEATHER_API_KEY=your_key_here
YOUTUBE_API_KEY=your_key_here (optional)
DATABASE_URL=sqlite:///./weather.db
```

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

API will be available at: **http://localhost:8000**
Docs at: **http://localhost:8000/docs**

## 📡 API Endpoints

### Weather Requests

#### Create Weather Request
```bash
POST /api/weather-requests/

Request body:
{
  "location": "San Francisco",
  "start_date": "2025-02-20",
  "end_date": "2025-02-25"
}

Response (201 Created):
{
  "id": 1,
  "raw_location": "San Francisco",
  "resolved_location": "San Francisco, US",
  "latitude": 37.7749,
  "longitude": -122.4194,
  "start_date": "2025-02-20",
  "end_date": "2025-02-25",
  "weather_payload": {...},
  "extra_payload": {"youtube_videos": [...]},
  "source": "openweathermap",
  "created_at": "2025-02-20T10:30:00",
  "updated_at": "2025-02-20T10:30:00"
}
```

#### List All Weather Requests
```bash
GET /api/weather-requests/?skip=0&limit=50

Response (200 OK):
[{...}, {...}]
```

#### Get Specific Request
```bash
GET /api/weather-requests/1

Response (200 OK):
{...}
```

#### Update Weather Request
```bash
PUT /api/weather-requests/1

Request body:
{
  "start_date": "2025-02-21",
  "end_date": "2025-02-26"
}

Response (200 OK):
{...updated record...}
```

#### Delete Weather Request
```bash
DELETE /api/weather-requests/1

Response (204 No Content)
```

### Data Export

#### Export as CSV
```bash
GET /api/exports/weather-requests.csv

Response: CSV file download
Columns: id, raw_location, resolved_location, latitude, longitude, start_date, end_date, source, created_at
```

#### Export as JSON
```bash
GET /api/exports/weather-requests.json

Response (200 OK):
[
  {
    "id": 1,
    "raw_location": "San Francisco",
    "resolved_location": "San Francisco, US",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "start_date": "2025-02-20",
    "end_date": "2025-02-25",
    "source": "openweathermap",
    "created_at": "2025-02-20T10:30:00",
    "weather_payload": {...},
    "extra_payload": {...}
  }
]
```

## 🔧 Database

### Models

**WeatherRequest**
- `id` (Integer): Primary key
- `raw_location` (String): User input
- `resolved_location` (String): Validated location (city, country)
- `latitude` (Float): Geographic latitude
- `longitude` (Float): Geographic longitude
- `start_date` (String): ISO date format
- `end_date` (String): ISO date format
- `weather_payload` (JSON): Raw API response
- `extra_payload` (JSON): YouTube videos and other data
- `source` (String): API source identifier
- `created_at` (DateTime): Record creation timestamp
- `updated_at` (DateTime): Record update timestamp

## ❌ Error Handling

The API returns meaningful HTTP status codes and messages:

- **400 Bad Request**: Invalid input or date range
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: Unexpected server error
- **502/503**: External API failure

### Example Error Response
```json
{
  "detail": "Location not found. Please check your spelling and try again."
}
```

## 🔑 Configuration

### Environment Variables (`.env`)

```env
# API Keys
OPENWEATHER_API_KEY=your_openweathermap_key
YOUTUBE_API_KEY=your_youtube_api_key  # Optional

# Database
DATABASE_URL=sqlite:///./weather.db
# Or for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/weather_db

# Application
APP_NAME=Weather Intelligence API
APP_VERSION=0.1.0
```

## 🧪 Testing

Test with curl:

```bash
# Create request
curl -X POST "http://localhost:8000/api/weather-requests/" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "London",
    "start_date": "2025-02-20",
    "end_date": "2025-02-25"
  }'

# List requests
curl "http://localhost:8000/api/weather-requests/"

# Export CSV
curl "http://localhost:8000/api/exports/weather-requests.csv" \
  -o weather_data.csv

# Export JSON
curl "http://localhost:8000/api/exports/weather-requests.json" \
  -o weather_data.json
```

## 🎓 How to Scale for AI/ML

This architecture is designed to support AI features:

1. **Historical Data Training**
   - Export accumulated weather data for ML models
   - Train risk prediction models on weather patterns

2. **LLM Integration**
   - Use stored weather + YouTube data as context
   - Generate natural language travel recommendations

3. **Real-Time Predictions**
   - Score weather risk levels for travel planning
   - Suggest alternative locations based on conditions

4. **Analytics Pipeline**
   - Track seasonal weather patterns
   - Build user preference models

## 📝 Assessment Requirements Met

✅ **Backend Engineer (Tech Assessment #2)**
- [x] Weather data retrieval from external API
- [x] Location validation (fuzzy matching supported)
- [x] Full CRUD operations with date range validation
- [x] Database persistence with SQLAlchemy
- [x] YouTube API integration for location content
- [x] CSV and JSON export functionality
- [x] Error handling with validation
- [x] Professional project structure
- [x] OpenAPI documentation

## 🚀 Future Enhancements

- [ ] User authentication with JWT
- [ ] Pagination and filtering for list endpoints
- [ ] WebSocket support for real-time updates
- [ ] Caching layer (Redis)
- [ ] Rate limiting
- [ ] Async database queries
- [ ] Unit and integration tests
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Additional API integrations (Maps, Weather Alerts)

## 📚 Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Async HTTP**: HTTPX
- **Validation**: Pydantic
- **Server**: Uvicorn

## 📄 License

Built for PM Accelerator AI Engineer Internship Assessment.

## 👤 Author

**Ragnork018**
- GitHub: [@Ragnork018](https://github.com/Ragnork018)
- LinkedIn: [your-linkedin-url]
- Portfolio: [your-portfolio-url]

## 🤝 Support

For questions or issues, please open a GitHub issue.

---

**Built with ❤️ for PM Accelerator**
