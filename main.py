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


def calculate_rsi(data, period=14):
    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.iloc[-1]


async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    coins = {
        "BTC": "BTC-USD",
        "ETH": "ETH-USD",
        "SOL": "SOL-USD",
        "BNB": "BNB-USD",
        "XRP": "XRP-USD"
    }

    message = "🔍 اسکن بازار:\n\n"

    for name, symbol in coins.items():

        try:
            data = yf.Ticker(symbol).history(period="1mo")

            price = data["Close"].iloc[-1]
            rsi = calculate_rsi(data)

            if rsi > 60:
                status = "🟢 قدرت خریدار"
            elif rsi < 40:
                status = "🔴 ضعیف"
            else:
                status = "🟡 صبر"

            message += (
                f"{name}\n"
                f"💰 قیمت: {price:.2f}\n"
                f"📊 RSI: {rsi:.2f}\n"
                f"وضعیت: {status}\n\n"
            )

        except Exception as e:
            message += f"{name}: خطا\n"


    await update.message.reply_text(message)


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("scan", scan))

app.run_polling()
