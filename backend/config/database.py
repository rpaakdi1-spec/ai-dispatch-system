from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from config.settings import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create declarative base for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Dependency for getting async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        # Import all models here to ensure they are registered
        from models import vehicle, client, order, gps_log
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        
        # Enable PostGIS extension if not exists
        await conn.execute("CREATE EXTENSION IF NOT EXISTS postgis;")


async def close_db():
    """Close database connections"""
    await engine.dispose()
