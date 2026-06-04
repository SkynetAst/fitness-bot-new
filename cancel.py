from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


async def cmd_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Действие отменено. Чем могу помочь?")
    return ConversationHandler.END
