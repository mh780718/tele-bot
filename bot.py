import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

SYSTEM_PROMPT = """
أنت Study Explainer:
تشرح كل شيء بطريقة تعليمية، خطوة بخطوة، وبأمثلة،
وبلغة عربية واضحة وبسيطة.
"""
def ask_deepseek(message):
    if not DEEPSEEK_API_KEY:
        return "❌ لم يتم وضع مفتاح DeepSeek في Render."

    url = "https://api.deepseek.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ]
    }

    try:
        r = requests.post(url, headers=headers, json=data, timeout=60)
        return f"🔎 DeepSeek HTTP {r.status_code}: {r.text}"
    except Exception as e:
        return f"❌ اتصال فشل: {str(e)}"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 mhnd أنا مدرسك الذكي Study Explainer. اسألني أي شيء!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("⏳ أفكر...")

    try:
        reply = ask_deepseek(user_text)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("❌ DeepSeek لا يرد الآن. تحقق من المفتاح.")
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot running...")
app.run_polling()
