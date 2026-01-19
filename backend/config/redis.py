import redis.asyncio as redis
from typing import Optional
from config.settings import get_settings

settings = get_settings()

# Redis client instance
redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """Get Redis client instance"""
    global redis_client
    
    if redis_client is None:
        redis_client = await redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            encoding="utf-8",
            decode_responses=True,
            max_connections=10,
        )
    
    return redis_client


async def close_redis():
    """Close Redis connection"""
    global redis_client
    
    if redis_client:
        await redis_client.close()
        redis_client = None


class RedisCache:
    """Redis cache wrapper with TTL support"""
    
    def __init__(self, ttl: int = None):
        self.ttl = ttl or settings.REDIS_CACHE_TTL
    
    async def get(self, key: str) -> Optional[str]:
        """Get value from cache"""
        client = await get_redis()
        return await client.get(key)
    
    async def set(self, key: str, value: str, ttl: int = None) -> bool:
        """Set value in cache with TTL"""
        client = await get_redis()
        expire_time = ttl or self.ttl
        return await client.setex(key, expire_time, value)
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        client = await get_redis()
        return await client.delete(key) > 0
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        client = await get_redis()
        return await client.exists(key) > 0
    
    async def set_json(self, key: str, value: dict, ttl: int = None) -> bool:
        """Set JSON value in cache"""
        import json
        return await self.set(key, json.dumps(value), ttl)
    
    async def get_json(self, key: str) -> Optional[dict]:
        """Get JSON value from cache"""
        import json
        value = await self.get(key)
        return json.loads(value) if value else None
