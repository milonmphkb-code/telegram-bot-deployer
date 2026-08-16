from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from bot.database.database import get_session
from bot.database.repository import PlanRepository, UserRepository
from bot.keyboards.user import (
    CB_BACK_TO_MENU,
    CB_DEPLOY_BOT,
    CB_MY_BOTS,
    CB_PLANS,
    CB_SERVER_STATUS,
    CB_SUPPORT,
    back_to_menu_keyboard,
    main_menu_keyboard,
)
from bot.utils.logger import logger

router = Router(name="user")

WELCOME_TEXT = (
    "👋 <b>স্বাগতম Telegram Bot Deployer-এ!</b>\n\n"
    "এই bot দিয়ে আপনি নিজের Telegram bot খুব সহজে deploy করতে পারবেন। "
    "নিচের মেনু থেকে একটি অপশন বেছে নিন।"
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    async with get_session() as session:
        users = UserRepository(session)
        user = await users.get_or_create(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name,
        )
        if user.is_banned:
            await message.answer("🚫 আপনি এই bot ব্যবহার করা থেকে নিষিদ্ধ (banned)।")
            return

    logger.info("User %s (%s) started the bot", message.from_user.id, message.from_user.username)
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == CB_BACK_TO_MENU)
async def cb_back_to_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == CB_PLANS)
async def cb_plans(callback: CallbackQuery) -> None:
    async with get_session() as session:
        plans = await PlanRepository(session).list_active()

    if not plans:
        text = "📋 <b>Plans</b>\n\nবর্তমানে কোনো active plan নেই। Admin শীঘ্রই plan যোগ করবেন।"
    else:
        lines = ["📋 <b>Available Plans</b>\n"]
        for plan in plans:
            lines.append(
                f"• <b>{plan.name}</b> — ৳{plan.price} / {plan.duration_days} days\n"
                f"   CPU: {plan.cpu_limit} | RAM: {plan.ram_limit_mb}MB | "
                f"Storage: {plan.storage_limit_mb}MB | Max Bots: {plan.max_bots}"
            )
        text = "\n".join(lines)

    await callback.message.edit_text(text, reply_markup=back_to_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == CB_DEPLOY_BOT)
async def cb_deploy_bot(callback: CallbackQuery) -> None:
    # Full deploy flow (plan -> payment -> zip upload -> token -> config)
    # ships in Phase 2/3/4. For now this confirms the entry point works.
    await callback.message.edit_text(
        "🚀 <b>Deploy Bot</b>\n\n"
        "📋 Step 1/5 Select your plan.\n\n"
        "⚠️ Plan selection ও deployment flow পরবর্তী phase-এ যুক্ত হবে।",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == CB_MY_BOTS)
async def cb_my_bots(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "🤖 <b>My Bots</b>\n\nআপনার এখনো কোনো deployed bot নেই।",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == CB_SERVER_STATUS)
async def cb_server_status(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "🖥 <b>Server Status</b>\n\n"
        "⚠️ Live resource monitoring পরবর্তী phase-এ (worker/server module) যুক্ত হবে।",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == CB_SUPPORT)
async def cb_support(callback: CallbackQuery) -> None:
    from bot.config import settings

    contact = f"@{settings.SUPPORT_USERNAME}" if settings.SUPPORT_USERNAME else "admin"
    await callback.message.edit_text(
        f"🎟 <b>Support</b>\n\nসাহায্যের জন্য যোগাযোগ করুন: {contact}",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()
