from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "AI Dispatch System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_CACHE_TTL: int = 3600
    
    # Naver Maps API
    NAVER_MAP_CLIENT_ID: str
    NAVER_MAP_CLIENT_SECRET: str
    NAVER_MAP_GEOCODE_URL: str = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    NAVER_MAP_DIRECTIONS_URL: str = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
    
    # Samsung UVIS API
    UVIS_API_URL: str = "https://api.s1.co.kr/uvis/v1"
    UVIS_API_KEY: str = "your_uvis_api_key_here"
    UVIS_POLL_INTERVAL: int = 30
    
    # OR-Tools
    ORTOOLS_TIME_LIMIT_SECONDS: int = 300
    ORTOOLS_SOLUTION_LIMIT: int = 100
    
    # Business Rules
    DEFAULT_WORK_HOURS_START: str = "06:00"
    DEFAULT_WORK_HOURS_END: str = "20:00"
    MAX_DRIVING_HOURS_PER_DAY: int = 10
    LOADING_UNLOADING_TIME_MINUTES: int = 30
    SPEED_FACTOR: float = 0.8
    
    # Upload
    UPLOAD_DIR: str = "./data/uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: str = "xlsx,xls,csv"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: str = "*"
    CORS_HEADERS: str = "*"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS origins string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Convert allowed extensions string to list"""
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
