from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import yfinance as yf

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 ربات سیگنال امین فعال شد!")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 Pong! ربات آنلاین است.")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="1d")
    current_price = data["Close"].iloc[-1]
    
    await update.message.reply_text(
        f"₿ قیمت فعلی بیت‌کوین:\n{current_price:.2f} دلار"
    )

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("price", price))

app.run_polling()
