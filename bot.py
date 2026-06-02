import os
from dotenv import load_dotenv
from telegram.ext import Application, ApplicationBuilder, CommandHandler, CallbackQueryHandler
from database import init_db
from onboarding import build_onboarding_handler
from reset import cmd_reset, handle_reset_confirm, handle_reset_cancel
from profile import cmd_profile
from training import cmd_train
from today import cmd_today
from food_diary import build_food_handler
from help import cmd_help

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
        ("help",    "Список команд"),
    ])


def main() -> None:
    init_db()
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    app.add_handler(build_onboarding_handler())
    app.add_handler(build_food_handler())
    app.add_handler(CommandHandler("reset", cmd_reset))
    app.add_handler(CallbackQueryHandler(handle_reset_confirm, pattern="^reset_confirm$"))
    app.add_handler(CallbackQueryHandler(handle_reset_cancel,  pattern="^reset_cancel$"))
    app.add_handler(CommandHandler("profile", cmd_profile))
    app.add_handler(CommandHandler("train", cmd_train))
    app.add_handler(CommandHandler("today", cmd_today))
    app.add_handler(CommandHandler("help", cmd_help))
    app.run_polling()


if __name__ == "__main__":
    main()
