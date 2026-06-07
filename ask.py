import google.generativeai as genai
from telegram import Update
from telegram.ext import ContextTypes
from rag import search

_model = genai.GenerativeModel("gemini-3.1-flash-lite")


async def cmd_ask(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    if not ctx.args:
        await update.message.reply_text(
            "Напиши вопрос после команды. Например: /ask когда работает бассейн?"
        )
        return
    query = " ".join(ctx.args)
    chunks = search(query)
    context_text = "\n\n".join(chunks)
    prompt = (
        f"Контекст:\n{context_text}\n\n"
        f"Вопрос: {query}\n\n"
        "Ответь кратко и только на основе контекста. "
        "Если ответа в контексте нет — скажи об этом. "
        "Не используй Markdown-разметку."
    )
    try:
        response = await _model.generate_content_async(prompt)
        await update.message.reply_text(response.text)
    except Exception:
        await update.message.reply_text("Не удалось получить ответ. Попробуй позже.")
