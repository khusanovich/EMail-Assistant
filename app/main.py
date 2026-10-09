"""FastAPI main application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print("Starting JobMail Assistant...")
    yield
    # Shutdown
    print("Shutting down JobMail Assistant...")


app = FastAPI(
    title="JobMail Assistant",
    description="Personal AI assistant for email monitoring and job application tracking",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "JobMail Assistant API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
