"""
Entry point — Main Telegram Bot (Phase 1: core skeleton).
Run: python main.py
"""
from __future__ import annotations

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import settings
from bot.database.database import init_db
from bot.handlers import user as user_handlers
from bot.utils.logger import logger


async def main() -> None:
    logger.info("Initializing database...")
    await init_db()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    dp.include_router(user_handlers.router)

    logger.info("Bot starting (polling mode)...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
