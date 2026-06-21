"""
TibbWell Backend API
FastAPI application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
from datetime import datetime

# Import routers
from api.auth import router as auth_router, pwd_context
from api.quiz import router as quiz_router
from api.premium import router as premium_router
from api.admin import router as admin_router
from api.chatbot import router as chatbot_router

# Application configuration
app = FastAPI(
    title="TibbWell API",
    description="Backend API for TibbWell - Traditional Unani Medicine Health Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS configuration - allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(quiz_router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(premium_router, prefix="/api/premium", tags=["Premium"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["Chatbot"])


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return JSONResponse(
        status_code=200,
        content={
            "name": "TibbWell API",
            "version": "1.0.0",
            "status": "running",
            "docs": "/api/docs"
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "tibbwell-backend"
        }
    )


@app.get("/api/health")
async def api_health_check():
    """
    API health check with external service status
    
    Reports the health status of:
    - Local API service
    - PayFast payment service (if configured)
    """
    health_status = {
        "status": "healthy",
        "service": "tibbwell-backend",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "external_services": {}
    }
    
    # Check PayFast health
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("https://api.payfast.co.za/health")
            if response.status_code == 200:
                health_status["external_services"]["payfast"] = {
                    "status": "healthy",
                    "latency_ms": round(response.elapsed.total_seconds() * 1000, 2)
                }
            else:
                health_status["external_services"]["payfast"] = {
                    "status": "degraded",
                    "status_code": response.status_code
                }
    except httpx.TimeoutException:
        health_status["external_services"]["payfast"] = {
            "status": "timeout",
            "error": "Connection timeout"
        }
        health_status["status"] = "degraded"
    except httpx.ConnectError:
        health_status["external_services"]["payfast"] = {
            "status": "unavailable",
            "error": "Connection failed"
        }
        health_status["status"] = "degraded"
    except Exception as e:
        health_status["external_services"]["payfast"] = {
            "status": "unknown",
            "error": str(e)
        }
    
    # Check database connectivity (basic query)
    try:
        from api.database import SessionLocal, User
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        health_status["database"] = {"status": "healthy"}
    except Exception as e:
        health_status["database"] = {"status": "error", "error": str(e)}
        health_status["status"] = "degraded"
    
    return JSONResponse(
        status_code=200 if health_status["status"] == "healthy" else 503,
        content=health_status
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )