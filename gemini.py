import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ContextTypes

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
_SYSTEM = (
    "Ты — фитнес-ассистент в Telegram-боте. Помогаешь пользователям с вопросами "
    "о питании, КБЖУ (калории, белки, жиры, углеводы), тренировках и здоровом образе "
    "жизни. Отвечай кратко и по делу — это мессенджер, не статья. "
    "Если вопрос не про фитнес или питание — мягко напомни, чем занимаешься. "
    "Не используй Markdown-разметку: никаких звёздочек, решёток, подчёркиваний — только plain text."
)
_model = genai.GenerativeModel("gemini-3.1-flash-lite", system_instruction=_SYSTEM)


async def handle_gemini(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        response = await _model.generate_content_async(update.message.text)
        await update.message.reply_text(response.text)
    except Exception:
        await update.message.reply_text("Не удалось получить ответ. Попробуй позже.")
