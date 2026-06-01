from datetime import date as date_today

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from database import add_food_entry

ASK_FOOD, ASK_GRAMS, ASK_CUSTOM_GRAMS = range(3)

FOOD_DB = {
    # Крупы
    "гречка": 313,
    "рис": 344,
    "овсянка": 389,
    "макароны": 350,
    "перловка": 320,
    "пшено": 342,
    # Мясо
    "куриная грудка": 110,
    "куриное бедро": 185,
    "говядина": 187,
    "свинина": 242,
    "фарш говяжий": 254,
    "индейка": 84,
    # Молочка
    "творог 5%": 121,
    "творог 0%": 71,
    "кефир": 51,
    "яйцо": 155,
    "молоко 3.2%": 60,
    "сыр": 360,
    "сметана 15%": 158,
    "йогурт": 66,
    # Овощи
    "огурец": 15,
    "помидор": 20,
    "капуста": 27,
    "морковь": 35,
    "картофель": 80,
    "перец болгарский": 27,
    "лук": 41,
    "свёкла": 43,
    "брокколи": 34,
    "шпинат": 23,
    # Фрукты
    "яблоко": 52,
    "банан": 96,
    "апельсин": 43,
    "виноград": 69,
    "груша": 57,
    "клубника": 33,
    # Рыба
    "лосось": 208,
    "тунец": 96,
    "треска": 82,
    "минтай": 72,
    "скумбрия": 191,
    # Хлеб
    "белый хлеб": 265,
    "чёрный хлеб": 210,
    # Орехи
    "грецкий орех": 654,
    "миндаль": 579,
    "арахис": 567,
    # Готовые блюда
    "борщ": 50,
    "пельмени": 275,
    "гречка с куриной грудкой": 175,
    # Прочее
    "масло сливочное": 748,
    "масло растительное": 899,
    "сахар": 399,
    "мёд": 329,
}


async def cmd_eat(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    ctx.user_data["user_id"] = update.effective_user.id
    await update.message.reply_text("Что ел? Напиши название продукта:")
    return ASK_FOOD


async def handle_food_name(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    name = update.message.text.strip().lower()
    if name not in FOOD_DB:
        await update.message.reply_text(
            "Продукт не найден. Попробуй другое название\n"
            "(например: гречка, куриная грудка) или /cancel"
        )
        return ASK_FOOD
    ctx.user_data["food_name"] = name
    ctx.user_data["kcal_per_100g"] = FOOD_DB[name]
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("100г", callback_data="grams_100"),
        InlineKeyboardButton("150г", callback_data="grams_150"),
        InlineKeyboardButton("200г", callback_data="grams_200"),
        InlineKeyboardButton("300г", callback_data="grams_300"),
        InlineKeyboardButton("Другое", callback_data="grams_other"),
    ]])
    await update.message.reply_text("Сколько грамм?", reply_markup=keyboard)
    return ASK_GRAMS


async def handle_grams(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    if query.data == "grams_other":
        await query.edit_message_text("Введи вес в граммах:")
        return ASK_CUSTOM_GRAMS
    grams = int(query.data.split("_")[1])
    return await _save_entry(query.edit_message_text, ctx, grams)


async def handle_custom_grams(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        grams = float(update.message.text.replace(",", "."))
    except ValueError:
        await update.message.reply_text("Введи положительное число, например: 250")
        return ASK_CUSTOM_GRAMS
    if grams <= 0:
        await update.message.reply_text("Введи положительное число, например: 250")
        return ASK_CUSTOM_GRAMS
    return await _save_entry(update.message.reply_text, ctx, grams)


async def _save_entry(send_fn, ctx: ContextTypes.DEFAULT_TYPE, grams: float) -> int:
    ud = ctx.user_data
    calories = round(ud["kcal_per_100g"] * grams / 100)
    add_food_entry(
        user_id=ud["user_id"],
        food_name=ud["food_name"],
        grams=grams,
        calories=calories,
        date=date_today.today().isoformat(),
    )
    await send_fn(f"✅ Записал: {ud['food_name']} {grams:.0f}г — {calories} ккал")
    return ConversationHandler.END


async def cancel_food(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Запись отменена.")
    return ConversationHandler.END


def build_food_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("eat", cmd_eat)],
        states={
            ASK_FOOD:         [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_food_name)],
            ASK_GRAMS:        [CallbackQueryHandler(handle_grams, pattern="^grams_")],
            ASK_CUSTOM_GRAMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_grams)],
        },
        fallbacks=[CommandHandler("cancel", cancel_food)],
    )
