import os
from dotenv import load_dotenv
from telegram.ext import Application, ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from database import init_db
from onboarding import build_onboarding_handler
from reset import cmd_reset, handle_reset_confirm, handle_reset_cancel
from profile import cmd_profile
from training import cmd_train
from today import cmd_today
from food_diary import build_food_handler
from help import cmd_help
from cancel import cmd_cancel
from gemini import handle_gemini

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


async def post_init(app: Application) -> None:
    await app.bot.set_my_commands([
        ("start",   "Начать / вернуться в меню"),
        ("profile", "Мой профиль и КБЖУ"),
        ("eat",     "Записать приём пищи"),
        ("today",   "Сводка питания за сегодня"),
        ("train",   "План тренировок"),
        ("reset",   "Сбросить профиль"),
        ("cancel",  "Отменить текущее действие"),
        ("help",    "Список команд"),
    ])


def main() -> None:
    init_db()
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    onboarding_h = build_onboarding_handler()
    food_h = build_food_handler()
    app.add_handler(onboarding_h)
    app.add_handler(food_h)
    app.bot_data["conv_handlers"] = [onboarding_h, food_h]
    app.add_handler(CommandHandler("reset", cmd_reset))
    app.add_handler(CallbackQueryHandler(handle_reset_confirm, pattern="^reset_confirm$"))
    app.add_handler(CallbackQueryHandler(handle_reset_cancel,  pattern="^reset_cancel$"))
    app.add_handler(CommandHandler("profile", cmd_profile))
    app.add_handler(CommandHandler("train", cmd_train))
    app.add_handler(CommandHandler("today", cmd_today))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("cancel", cmd_cancel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gemini))
    app.run_polling()


if __name__ == "__main__":
    main()
