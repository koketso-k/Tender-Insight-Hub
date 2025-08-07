"""
Tender Insight Hub - Async SQL Engine
Database connection manager for MySQL/PostgreSQL with connection pooling and tenant isolation.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional
import logging
from .config import settings
from .sql_models import Base  # From your sql_models.py

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Async database connection manager with SaaS multi-tenant support"""
    
    def __init__(self):
        self.engine = None
        self.async_session = None
        self._initialized = False

    async def initialize(self):
        """Initialize database connection pool and verify connection"""
        try:
            # Determine dialect-specific connection options
            if settings.DB_ENGINE == "postgresql":
                connect_args = {}
                pool_size = settings.POSTGRES_POOL_SIZE
                db_url = (
                    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
                    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
                )
            else:  # MySQL
                connect_args = {"charset": "utf8mb4"}
                pool_size = settings.MYSQL_POOL_SIZE
                db_url = (
                    f"mysql+asyncmy://{settings.DB_USER}:{settings.DB_PASSWORD}@"
                    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
                )

            self.engine = create_async_engine(
                db_url,
                pool_size=pool_size,
                max_overflow=settings.DB_MAX_OVERFLOW,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=settings.SQL_ECHO,
                connect_args=connect_args
            )

            # Verify connection
            async with self.engine.begin() as conn:
                await conn.execute("SELECT 1")
            
            self.async_session = sessionmaker(
                self.engine,
                expire_on_commit=False,
                class_=AsyncSession
            )
            
            self._initialized = True
            logger.info(
                f"{settings.DB_ENGINE.upper()} connection pool initialized "
                f"with size {pool_size}"
            )
            
        except SQLAlchemyError as e:
            logger.error("Database connection failed: %s", str(e))
            raise

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """Context manager for database sessions with automatic cleanup"""
        if not self._initialized:
            await self.initialize()
            
        session = self.async_session()
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error("Database operation failed: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service temporarily unavailable"
            )
        finally:
            await session.close()

    async def create_tables(self):
        """Initialize database schema (for first-time setup)"""
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created")
        except SQLAlchemyError as e:
            logger.error("Schema creation failed: %s", str(e))
            raise

    async def drop_tables(self):
        """Drop all tables (for testing only)"""
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            logger.warning("Database tables dropped")
        except SQLAlchemyError as e:
            logger.error("Schema drop failed: %s", str(e))
            raise

    # ---- Tenant Isolation Helpers ----
    async def execute_for_tenant(self, tenant_id: str, stmt, session: AsyncSession):
        """Add tenant_id filter to all queries"""
        if not hasattr(stmt, 'where'):
            return await session.execute(stmt)
            
        tenant_condition = getattr(stmt.table.columns, 'tenant_id') == tenant_id
        stmt = stmt.where(tenant_condition)
        return await session.execute(stmt)

    async def close(self):
        """Cleanup connection pool"""
        if self.engine:
            await self.engine.dispose()
            self._initialized = False
            logger.info("Database connection pool closed")

# Singleton instance for dependency injection
db_manager = DatabaseManager()

async def init_db():
    """Initialize database on startup"""
    await db_manager.initialize()
    if settings.CREATE_TABLES:
        await db_manager.create_tables()

async def close_db():
    """Cleanup database on shutdown"""
    await db_manager.close()