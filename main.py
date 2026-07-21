from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong!")

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("ping", ping))

app.run_polling()
