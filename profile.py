from telegram import Update
from telegram.ext import ContextTypes
from database import get_user
from kbzhu import calculate_kbzhu

_GOAL_DISPLAY = {
    "похудеть": "Похудеть",
    "поддержать вес": "Поддержать вес",
    "набрать массу": "Набрать массу",
}


async def cmd_profile(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user = get_user(update.effective_user.id)
    if not user:
        await update.message.reply_text("Сначала пройди /start")
        return

    k = calculate_kbzhu(
        user["height"], user["weight"], user["age"], user["gender"], user["goal"]
    )
    text = (
        "👤 Твой профиль:\n\n"
        f"📏 Рост: {user['height']:.0f} см\n"
        f"⚖️ Вес: {user['weight']:.0f} кг\n"
        f"🎂 Возраст: {user['age']} лет\n"
        f"🚻 Пол: {user['gender'].capitalize()}\n"
        f"🎯 Цель: {_GOAL_DISPLAY.get(user['goal'], user['goal'])}\n\n"
        f"🔥 Калории: {k['calories']} ккал\n"
        f"💪 Белки: {k['protein']} г\n"
        f"🥑 Жиры: {k['fat']} г\n"
        f"🍞 Углеводы: {k['carbs']} г"
    )
    await update.message.reply_text(text)
