"""
Async SQLAlchemy engine/session setup.
Works with both sqlite+aiosqlite (local dev) and postgresql+asyncpg (production)
based on DATABASE_URL — no code change needed to switch.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from bot.config import settings
from bot.database.models import Base

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Creates tables if they don't exist yet.
    For production use Alembic migrations instead of this (Phase 2 adds
    the Alembic setup) — this is convenient for local/dev bootstrapping.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
