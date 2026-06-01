import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from database import init_db
from onboarding import build_onboarding_handler
from reset import cmd_reset, handle_reset_confirm, handle_reset_cancel
from profile import cmd_profile
from training import cmd_train

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


def main() -> None:
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(build_onboarding_handler())
    app.add_handler(CommandHandler("reset", cmd_reset))
    app.add_handler(CallbackQueryHandler(handle_reset_confirm, pattern="^reset_confirm$"))
    app.add_handler(CallbackQueryHandler(handle_reset_cancel,  pattern="^reset_cancel$"))
    app.add_handler(CommandHandler("profile", cmd_profile))
    app.add_handler(CommandHandler("train", cmd_train))
    app.run_polling()


if __name__ == "__main__":
    main()
