"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app import __version__, __author__, __project__
from app.config import settings
from app.database import Base, engine

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup and shutdown."""
    # Startup: Create database tables
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialization completed.")
    yield
    # Shutdown: Clean up resources
    logger.info("Shutting down application...")


# Create FastAPI application instance
app = FastAPI(
    title="Weather Intelligence Backend API",
    description="Professional-grade FastAPI backend for weather intelligence",
    version=__version__,
    contact={
        "name": __author__,
        "url": "https://github.com/Ragnork018",
    },
    lifespan=lifespan,
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check and information."""
    return {
        "message": "Weather Intelligence Backend API",
        "version": __version__,
        "author": __author__,
        "project": __project__,
        "status": "running",
        "documentation": "/docs",
        "openapi_schema": "/openapi.json",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "version": __version__,
        "message": "API is operational",
    }


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {__project__} v{__version__}...")
    logger.info(f"Host: {settings.HOST}, Port: {settings.PORT}, Debug: {settings.DEBUG}")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
