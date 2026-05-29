"""
Main FastAPI application entry point.
"""

# Import FastAPI framework
from fastapi import FastAPI

# Import versioned API router
from src.api.v1.router import api_router


# Create FastAPI application instance
# 'title' appears in Swagger/OpenAPI documentation
app = FastAPI(title="Lobang API")


@app.get("/health")
def health_check():
    """
    Health check endpoint.

    Used to verify that the API server is running.
    Commonly used by:
    - monitoring systems
    - Docker/Kubernetes health checks
    - load balancers
    """

    # Simple JSON response
    return {"status": "ok"}


# Register API routes under versioned prefix
# Example: /api/v1/deals
app.include_router(api_router, prefix="/api/v1")