import logging
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters


# 1. ដាក់ Telegram Token និង Gemini API Key របស់អ្នកនៅទីនេះ
TELEGRAM_TOKEN = "8767848278:AAHqNUJhPie0tR31O6jx8yXUUCbHfEWngEo"
GEMINI_API_KEY = "AIzaSyCdAgjUTGNvrFXNGKx2CP7BJ_bjJmmk68w"


# កំណត់រចនាសម្ព័ន្ធ Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# មុខងារស្វាគមន៍ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("សួស្តី! ខ្ញុំជា Telegram Bot របស់អ្នកដែលដំណើរការដោយ Gemini AI (Python)។ តើមានអ្វីឱ្យខ្ញុំជួយថ្ងៃនេះ?")


# មុខងារទទួលសារ និងឆ្លើយតបស្វ័យប្រវត្តិជាមួយ Gemini
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        response = client.models.generate_content(
    model='gemini-1.5-flash',
    contents=user_text,
)
        ai_reply = response.text
        await update.message.reply_text(ai_reply)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("សូមអភ័យទោស មានបញ្ហាក្នុងการតភ្ជាប់ជាមួយ Gemini AI។")


if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🤖 Bot កំពុងដំណើរការ... (ចុច Ctrl+C ដើម្បីបិទ)")
    app.run_polling()