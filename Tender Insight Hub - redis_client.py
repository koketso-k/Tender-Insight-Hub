"""
Tender Insight Hub - Redis Client Manager
Handles all Redis operations with connection pooling and error handling.
"""

import redis.asyncio as redis
from redis.exceptions import RedisError
from fastapi import HTTPException, status
from contextlib import asynccontextmanager
from typing import Optional, AsyncIterator, Union
import logging
from datetime import timedelta
from .config import settings

logger = logging.getLogger(__name__)

class RedisClient:
    """Thread-safe Redis connection manager with SaaS tenant isolation"""
    
    def __init__(self):
        self.pool: Optional[redis.ConnectionPool] = None
        self.rate_limit_window = 60  # seconds
        self.max_connections = 20

    async def initialize(self):
        """Create connection pool on startup"""
        self.pool = redis.ConnectionPool.from_url(
            settings.REDIS_URL,
            max_connections=self.max_connections,
            decode_responses=True
        )
        logger.info(f"Redis connection pool initialized with {self.max_connections} connections")

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[redis.Redis]:
        """Context manager for Redis connections"""
        if not self.pool:
            await self.initialize()
            
        conn = redis.Redis(connection_pool=self.pool)
        try:
            yield conn
        except RedisError as e:
            logger.error(f"Redis operation failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Cache service temporarily unavailable"
            )
        finally:
            await conn.close()

    # ---- Core Caching Methods ----
    async def set_cache(
        self, 
        key: str, 
        value: Union[str, dict, list],
        ttl: Optional[int] = None,
        tenant_id: Optional[str] = None
    ) -> bool:
        """Cache data with tenant isolation and TTL"""
        cache_key = f"tenant:{tenant_id}:{key}" if tenant_id else key
        async with self.get_connection() as conn:
            try:
                if isinstance(value, (dict, list)):
                    return await conn.json().set(cache_key, "$", value, ex=ttl)
                return await conn.set(cache_key, value, ex=ttl)
            except RedisError as e:
                logger.warning(f"Cache set failed for {cache_key}: {str(e)}")
                return False

    async def get_cache(
        self,
        key: str,
        tenant_id: Optional[str] = None
    ) -> Optional[Union[str, dict, list]]:
        """Retrieve cached data with tenant isolation"""
        cache_key = f"tenant:{tenant_id}:{key}" if tenant_id else key
        async with self.get_connection() as conn:
            try:
                # Attempt JSON decode first
                if (result := await conn.json().get(cache_key)) is not None:
                    return result
                # Fallback to string
                return await conn.get(cache_key)
            except RedisError:
                return None

    # ---- Rate Limiting ----
    async def check_rate_limit(
        self,
        identifier: str,
        limit: int = 100,
        window: Optional[int] = None
    ) -> dict:
        """Sliding window rate limiting"""
        window = window or self.rate_limit_window
        async with self.get_connection() as conn:
            try:
                current = await conn.incr(f"rate_limit:{identifier}")
                if current == 1:
                    await conn.expire(f"rate_limit:{identifier}", window)
                remaining = max(0, limit - current)
                return {
                    "limit": limit,
                    "remaining": remaining,
                    "reset": window
                }
            except RedisError:
                return {"limit": 0, "remaining": limit, "reset": window}

    # ---- SaaS Multi-Tenant Features ----
    async def invalidate_tenant_cache(self, tenant_id: str) -> int:
        """Clear all cached data for a tenant"""
        async with self.get_connection() as conn:
            keys = await conn.keys(f"tenant:{tenant_id}:*")
            if keys:
                return await conn.delete(*keys)
            return 0

    async def cache_tender_summary(
        self,
        tender_id: str,
        summary: dict,
        ttl: int = 86400  # 24 hours
    ) -> bool:
        """Cache AI-generated tender summaries"""
        return await self.set_cache(
            key=f"summary:{tender_id}",
            value=summary,
            ttl=ttl
        )

    async def get_cached_summary(self, tender_id: str) -> Optional[dict]:
        """Retrieve cached tender summary"""
        return await self.get_cache(f"summary:{tender_id}")

# Singleton instance for dependency injection
redis_client = RedisClient()

async def init_redis():
    """Initialize Redis on application startup"""
    await redis_client.initialize()

async def close_redis():
    """Cleanup Redis connections on shutdown"""
    if redis_client.pool:
        await redis_client.pool.disconnect()
        logger.info("Redis connection pool closed")