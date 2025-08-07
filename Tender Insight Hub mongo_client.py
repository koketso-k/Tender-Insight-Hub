"""
Tender Insight Hub - MongoDB Client Manager
Async MongoDB connection handling with tenant isolation and performance optimizations.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import PyMongoError
from fastapi import HTTPException, status
from contextlib import asynccontextmanager
from typing import Optional, AsyncIterator
import logging
from .config import settings
from .mongo_models import MONGO_INDEXES  # From your mongo_models.py

logger = logging.getLogger(__name__)

class MongoClient:
    """MongoDB connection manager with built-in tenant isolation"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None
        self._initialized = False

    async def initialize(self):
        """Initialize connection pool and ensure indexes"""
        try:
            self.client = AsyncIOMotorClient(
                settings.MONGO_URI,
                maxPoolSize=settings.MONGO_MAX_POOL_SIZE,
                minPoolSize=settings.MONGO_MIN_POOL_SIZE,
                serverSelectionTimeoutMS=5000,
                tls=settings.MONGO_TLS,
                tlsInsecure=settings.MONGO_TLS_INSECURE
            )
            
            # Verify connection
            await self.client.admin.command('ping')
            self.db = self.client[settings.MONGO_DB_NAME]
            
            # Ensure indexes
            await self._ensure_indexes()
            
            self._initialized = True
            logger.info("MongoDB connection established with %s pool size", 
                       settings.MONGO_MAX_POOL_SIZE)
            
        except PyMongoError as e:
            logger.error("MongoDB connection failed: %s", str(e))
            raise

    async def _ensure_indexes(self):
        """Create all predefined indexes"""
        try:
            for collection_name, indexes in MONGO_INDEXES.items():
                collection = self.db[collection_name]
                for index_spec in indexes:
                    await collection.create_index(index_spec[0], **index_spec[1] if len(index_spec) > 1 else {})
            logger.info("MongoDB indexes verified")
        except PyMongoError as e:
            logger.warning("Index creation failed: %s", str(e))

    @asynccontextmanager
    async def get_db(self) -> AsyncIterator[AsyncIOMotorDatabase]:
        """Context manager for database access"""
        if not self._initialized:
            await self.initialize()
            
        try:
            yield self.db
        except PyMongoError as e:
            logger.error("MongoDB operation failed: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service temporarily unavailable"
            )

    # ---- Tenant Isolation Helpers ----
    async def get_tenant_collection(self, collection_name: str, tenant_id: str):
        """Get a collection with tenant-specific prefix"""
        return self.db[f"tenant_{tenant_id}_{collection_name}"]

    # ---- Core Document Operations ----
    async def insert_summary(self, summary_data: dict) -> str:
        """Insert AI-generated tender summary"""
        try:
            async with self.get_db() as db:
                result = await db.tender_summaries.insert_one(summary_data)
                return str(result.inserted_id)
        except PyMongoError as e:
            logger.error("Failed to insert summary: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store document summary"
            )

    async def get_summary(self, tender_id: str) -> Optional[dict]:
        """Retrieve cached tender summary"""
        try:
            async with self.get_db() as db:
                return await db.tender_summaries.find_one({"tender_id": tender_id})
        except PyMongoError:
            return None

    async def get_readiness_scores(self, profile_id: str, limit: int = 10) -> list:
        """Get latest readiness scores for a company profile"""
        try:
            async with self.get_db() as db:
                cursor = db.readiness_scores.find(
                    {"profile_id": profile_id},
                    sort=[("generated_at", -1)],
                    limit=limit
                )
                return await cursor.to_list(length=limit)
        except PyMongoError:
            return []

    # ---- Analytics Operations ----
    async def get_cached_analytics(self, analysis_type: str) -> Optional[dict]:
        """Retrieve pre-computed analytics"""
        try:
            async with self.get_db() as db:
                return await db.cached_analytics.find_one(
                    {"analysis_type": analysis_type},
                    sort=[("last_updated", -1)]
                )
        except PyMongoError:
            return None

    async def close(self):
        """Cleanup connections"""
        if self.client:
            self.client.close()
            self._initialized = False
            logger.info("MongoDB connection closed")

# Singleton instance for dependency injection
mongo_client = MongoClient()

async def init_mongo():
    """Initialize MongoDB on startup"""
    await mongo_client.initialize()

async def close_mongo():
    """Cleanup MongoDB on shutdown"""
    await mongo_client.close()