from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import delete_user


async def cmd_reset(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Да, сбросить", callback_data="reset_confirm"),
        InlineKeyboardButton("Отмена",       callback_data="reset_cancel"),
    ]])
    await update.message.reply_text(
        "Ты уверен? Все твои данные будут удалены.",
        reply_markup=keyboard,
    )


async def handle_reset_confirm(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    delete_user(user_id)
    conv_key = (user_id, user_id)
    for handler in ctx.bot_data.get("conv_handlers", []):
        handler.conversations.pop(conv_key, None)
    await query.edit_message_text(
        "Данные удалены. Напиши /start чтобы начать заново."
    )


async def handle_reset_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Сброс отменён.")
