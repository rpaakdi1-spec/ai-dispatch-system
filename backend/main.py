from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import logging

from config import get_settings, init_db, close_db, close_redis
from config.settings import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings: Settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting AI Dispatch System...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    
    try:
        # Initialize database
        logger.info("Initializing database...")
        await init_db()
        logger.info("✅ Database initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
    
    logger.info(f"✅ AI Dispatch System started on http://{settings.HOST}:{settings.PORT}")
    logger.info(f"📖 API Documentation available at http://{settings.HOST}:{settings.PORT}/docs")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down AI Dispatch System...")
    
    try:
        await close_db()
        logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Error closing database: {e}")
    
    try:
        await close_redis()
        logger.info("✅ Redis connections closed")
    except Exception as e:
        logger.error(f"❌ Error closing Redis: {e}")
    
    logger.info("👋 AI Dispatch System shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## AI-Based Dispatch System for Frozen/Refrigerated Cargo
    
    ### Features:
    * 🚛 **Vehicle Management**: Manage fleet of 40+ refrigerated trucks
    * 📦 **Order Management**: Handle 110+ daily orders with temperature constraints
    * 🤖 **AI Dispatch**: Optimize routes using Google OR-Tools VRP solver
    * 🗺️ **Real-time GPS**: Track vehicles via Samsung UVIS integration
    * ❄️ **Temperature Monitoring**: Ensure cold chain compliance
    * 📊 **Analytics**: Real-time dashboard and performance metrics
    
    ### Temperature Types:
    * **Frozen** (-18°C ~ -25°C)
    * **Chilled** (0°C ~ 6°C)
    * **Ambient** (Room temperature)
    
    ### Optimization Goals:
    * Minimize empty running distance
    * Maximize pallet utilization
    * Ensure time window compliance
    * Balance workload across drivers
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=["*"] if settings.CORS_METHODS == "*" else settings.CORS_METHODS.split(","),
    allow_headers=["*"] if settings.CORS_HEADERS == "*" else settings.CORS_HEADERS.split(","),
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/api/info", tags=["Info"])
async def api_info():
    """API information and configuration"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "features": {
            "vehicle_management": True,
            "order_management": True,
            "ai_dispatch": True,
            "gps_tracking": bool(settings.UVIS_API_KEY != "your_uvis_api_key_here"),
            "naver_maps": bool(settings.NAVER_MAP_CLIENT_ID),
        },
        "limits": {
            "max_driving_hours": settings.MAX_DRIVING_HOURS_PER_DAY,
            "loading_time_minutes": settings.LOADING_UNLOADING_TIME_MINUTES,
            "max_upload_size_mb": settings.MAX_UPLOAD_SIZE_MB,
        },
        "optimization": {
            "time_limit_seconds": settings.ORTOOLS_TIME_LIMIT_SECONDS,
            "solution_limit": settings.ORTOOLS_SOLUTION_LIMIT,
        },
    }


# Import and include routers (will be created next)
# from routes import vehicles, clients, orders, dispatch, gps
# app.include_router(vehicles.router, prefix="/api/vehicles", tags=["Vehicles"])
# app.include_router(clients.router, prefix="/api/clients", tags=["Clients"])
# app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])
# app.include_router(dispatch.router, prefix="/api/dispatch", tags=["Dispatch"])
# app.include_router(gps.router, prefix="/api/gps", tags=["GPS"])


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred",
        }
    )


if __name__ == "__main__":
    """Run the application"""
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning",
    )
