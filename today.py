from datetime import date

from telegram import Update
from telegram.ext import ContextTypes
from database import get_user, get_today_entries


async def cmd_today(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user = get_user(user_id)
    if not user:
        await update.message.reply_text("Сначала пройди /start")
        return
    entries = get_today_entries(user_id, date.today().isoformat())
    if not entries:
        await update.message.reply_text("Сегодня ещё ничего не записано. Используй /eat")
        return
    lines = [
        f"• {e['food_name']} {e['grams']:.0f}г — {e['calories']:.0f} ккал"
        for e in entries
    ]
    total = sum(e["calories"] for e in entries)
    daily = user["daily_calories"]
    text = (
        "🍽 Питание за сегодня:\n\n"
        + "\n".join(lines)
        + f"\n\n📊 Итого: {total:.0f} / {daily:.0f} ккал"
    )
    await update.message.reply_text(text)
