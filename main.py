from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import yfinance as yf
import pandas as pd
import os
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
f"₿ قیمت فعلی بیت‌کوین:\n{current_price:,.2f} دلار"
)
def calculate_rsi(prices, period=14):
delta = prices.diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta 
