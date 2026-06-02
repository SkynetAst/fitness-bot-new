from telegram import Update
from telegram.ext import ContextTypes

HELP_TEXT = (
    "🤖 Вот что я умею:\n\n"
    "/profile — твой профиль и КБЖУ\n"
    "/eat — записать приём пищи\n"
    "/today — сводка питания за сегодня\n"
    "/train — план тренировок\n"
    "/reset — сбросить профиль\n"
    "/help — список команд"
)


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT)
