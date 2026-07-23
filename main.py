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
    data = btc.history(period="3mo")
    current_price = data["Close"].iloc[-1]

    await update.message.reply_text(
        f"₿ قیمت فعلی بیت‌کوین:\n{current_price:.2f} دلار"
    )


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
            data = yf.Ticker(symbol).history(period="1d")
            price = data["Close"].iloc[-1]
            message += f"{name}: {price:.2f} USD\n"
        except:
            message += f"{name}: خطا در دریافت قیمت\n"

    await update.message.reply_text(message)


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("scan", scan))

def calculate_rsi(series, period=14):
    delta = series.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi
    
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
btc = yf.Ticker("BTC-USD")
data = btc.history(period="3mo")
price = data["Close"].iloc[-1]
old = data["Close"].iloc[-2]
rsi = calculate_rsi(data["Close"]).iloc[-1]

if rsi < 30:
    sig = "🟢 BUY (RSI Oversold)"

elif rsi > 70:
    sig = "🔴 SELL (RSI Overbought)"

else:
    if price > old:
        sig = "🟢 BUY"

    elif price < old:
        sig = "🔴 SELL"

    else:
        sig = "🟡 WAIT"

text = f"₿ BTC: {price:.2f}$\n📊 RSI: {rsi:.1f}"

await update.message.reply_text(f"{text} | 🎯 {sig}")
app.add_handler(CommandHandler("signal", signal))

app.run_polling()


