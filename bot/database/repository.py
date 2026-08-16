"""
Repository layer — all raw DB queries live here so handlers never touch
SQLAlchemy directly. Every query is parameterized via the ORM (no raw SQL
string interpolation), which protects against SQL injection.
"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Plan, User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    async def get_or_create(self, telegram_id: int, username: str | None, full_name: str | None) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            return user
        user = User(telegram_id=telegram_id, username=username, full_name=full_name)
        self.session.add(user)
        await self.session.flush()
        return user

    async def is_banned(self, telegram_id: int) -> bool:
        user = await self.get_by_telegram_id(telegram_id)
        return bool(user and user.is_banned)


class PlanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_active(self) -> list[Plan]:
        result = await self.session.execute(
            select(Plan).where(Plan.is_active.is_(True)).order_by(Plan.price.asc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, plan_id: int) -> Plan | None:
        result = await self.session.execute(select(Plan).where(Plan.id == plan_id))
        return result.scalar_one_or_none()
