import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ContextTypes

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
_model = genai.GenerativeModel("gemini-3.1-flash-lite")


async def handle_gemini(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = await _model.generate_content_async(update.message.text)
        await update.message.reply_text(response.text)
    except Exception:
        await update.message.reply_text("Не удалось получить ответ. Попробуй позже.")
