from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from database import get_user, save_user, update_calories
from kbzhu import calculate_kbzhu
from help import HELP_TEXT
from cancel import cmd_cancel

HEIGHT, WEIGHT, AGE, GENDER, GOAL = range(5)

_GENDER_MAP = {"gender_male": "мужской", "gender_female": "женский"}
_GOAL_MAP = {
    "goal_lose": "похудеть",
    "goal_maintain": "поддержать вес",
    "goal_gain": "набрать массу",
}


async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    if get_user(user_id):
        name = update.effective_user.first_name
        keyboard = ReplyKeyboardMarkup(
            [["Мой профиль", "Дневник питания"]], resize_keyboard=True
        )
        await update.message.reply_text(
            f"С возвращением, {name}! 👋", reply_markup=keyboard
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "Привет! Я фитнес-бот 💪\nДавай познакомимся. Введи свой рост в см:"
    )
    return HEIGHT


async def ask_weight(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        value = float(update.message.text.replace(",", "."))
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи число. Например: 175")
        return HEIGHT
    if not 100 <= value <= 250:
        await update.message.reply_text("Рост должен быть от 100 до 250 см. Попробуй ещё раз:")
        return HEIGHT
    ctx.user_data["height"] = value
    await update.message.reply_text("Отлично! Теперь введи свой вес в кг:")
    return WEIGHT


async def ask_age(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        value = float(update.message.text.replace(",", "."))
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи число. Например: 70.5")
        return WEIGHT
    if not 30 <= value <= 300:
        await update.message.reply_text("Вес должен быть от 30 до 300 кг. Попробуй ещё раз:")
        return WEIGHT
    ctx.user_data["weight"] = value
    await update.message.reply_text("Хорошо! Введи свой возраст:")
    return AGE


async def ask_gender(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        value = int(update.message.text.strip())
    except ValueError:
        await update.message.reply_text("Пожалуйста, введи целое число. Например: 25")
        return AGE
    if not 10 <= value <= 100:
        await update.message.reply_text("Возраст должен быть от 10 до 100 лет. Попробуй ещё раз:")
        return AGE
    ctx.user_data["age"] = value
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Мужской", callback_data="gender_male"),
        InlineKeyboardButton("Женский", callback_data="gender_female"),
    ]])
    await update.message.reply_text("Укажи свой пол:", reply_markup=keyboard)
    return GENDER


async def ask_goal(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    ctx.user_data["gender"] = _GENDER_MAP[query.data]
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Похудеть", callback_data="goal_lose"),
        InlineKeyboardButton("Поддержать вес", callback_data="goal_maintain"),
        InlineKeyboardButton("Набрать массу", callback_data="goal_gain"),
    ]])
    await query.edit_message_text("Какова твоя цель?", reply_markup=keyboard)
    return GOAL


async def finish_onboarding(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    ud = ctx.user_data
    user_id = update.effective_user.id
    goal_str = _GOAL_MAP[query.data]
    save_user(
        user_id=user_id,
        height=ud["height"],
        weight=ud["weight"],
        age=ud["age"],
        gender=ud["gender"],
        goal=goal_str,
    )
    kbzhu = calculate_kbzhu(ud["height"], ud["weight"], ud["age"], ud["gender"], goal_str)
    update_calories(user_id, kbzhu["calories"])
    await query.edit_message_text(
        "🎉 Ты настроен! Твои данные сохранены.\n\n"
        + HELP_TEXT
    )
    return ConversationHandler.END


async def _cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Анкета отменена. Напиши /start чтобы начать заново.")
    return ConversationHandler.END


def build_onboarding_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("start", cmd_start)],
        states={
            HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_weight)],
            WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            AGE:    [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_gender)],
            GENDER: [CallbackQueryHandler(ask_goal,           pattern="^gender_")],
            GOAL:   [CallbackQueryHandler(finish_onboarding,  pattern="^goal_")],
        },
        fallbacks=[CommandHandler("cancel", cmd_cancel)],
        allow_reentry=True,
    )
