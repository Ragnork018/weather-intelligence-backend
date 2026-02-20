"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app import __version__, __author__, __project__
from app.config import settings
from app.database import Base, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup: Create database tables
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: Clean up resources
    logger.info("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title="Weather Intelligence Backend",
    description="Backend API for Weather Intelligence Application",
    version=__version__,
    contact={"name": __author__},
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "Weather Intelligence Backend API",
        "version": __version__,
        "author": __author__,
        "project": __project__,
        "status": "running"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": __version__
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
