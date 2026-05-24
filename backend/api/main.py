"""
TibbWell Backend API
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import routers
from api.auth import router as auth_router
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
    """API health check with more detail"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "tibbwell-backend",
            "version": "1.0.0"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )