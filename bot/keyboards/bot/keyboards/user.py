from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Callback data constants — shared between keyboards.py and handlers so they
# can never drift apart.
CB_DEPLOY_BOT = "menu:deploy_bot"
CB_MY_BOTS = "menu:my_bots"
CB_PLANS = "menu:plans"
CB_SERVER_STATUS = "menu:server_status"
CB_SUPPORT = "menu:support"
CB_BACK_TO_MENU = "menu:back"


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Deploy Bot", callback_data=CB_DEPLOY_BOT)],
            [InlineKeyboardButton(text="🤖 My Bots", callback_data=CB_MY_BOTS)],
            [InlineKeyboardButton(text="📋 Plans", callback_data=CB_PLANS)],
            [InlineKeyboardButton(text="🖥 Server Status", callback_data=CB_SERVER_STATUS)],
            [InlineKeyboardButton(text="🎟 Support", callback_data=CB_SUPPORT)],
        ]
    )


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ Back", callback_data=CB_BACK_TO_MENU)]]
    )
