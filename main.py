from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import yfinance as yf

BOT_TOKEN = os.getenv('BOT_TOKEN')

------------------ دستورات پایه ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text('🤖 ربات سیگنال امین فعال شد!')

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text('🏓 Pong! ربات آنلاین است.')

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
btc = yf.Ticker('BTC-USD')
data = btc.history(period='1d')
current_price = data['Close'].iloc[-1]

await update.message.reply_text(
    f'₿ قیمت فعلی بیت‌کوین:\\n{current_price:.2f} دلار'
)

------------------ محاسبه RSI ------------------

def calculate_rsi(data, period=14):
delta = data['Close'].diff()

gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(period).mean()
avg_loss = loss.rolling(period).mean()

rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

return rsi.iloc[-1]

------------------ اسکن بازار ------------------

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):

coins = {
    'BTC': 'BTC-USD',
    'ETH': 'ETH-USD',
    'SOL': 'SOL-USD',
    'BNB': 'BNB-USD',
    'XRP': 'XRP-USD',
    'ADA': 'ADA-USD',
    'LINK': 'LINK-USD',
    'DOGE': 'DOGE-USD',
    'AVAX': 'AVAX-USD',
    'DOT': 'DOT-USD',
    'MATIC': 'MATIC-USD',
    'LTC': 'LTC-USD'
}

results = []

for name, symbol in coins.items():

    try:
        data = yf.Ticker(symbol).history(period='3mo')

        current_price = data['Close'].iloc[-1]
        current_volume = data['Volume'].iloc[-1]

        rsi = calculate_rsi(data)
        ma20 = data['Close'].rolling(20).mean().iloc[-1]
        avg_volume = data['Volume'].rolling(20).mean().iloc[-1]

        score = 0
        reasons = []

        # RSI
        if rsi > 60:
            score += 3
            reasons.append('RSI قوی')
        elif rsi > 50:
            score += 1

        # MA20
        if current_price > ma20:
            score += 3
            reasons.append('بالای MA20')

        # حجم
        if current_volume > avg_volume:
            score += 4
            reasons.append('حجم تایید شد')

        score = max(0, min(score, 10))

        results.append({
            'name': name,
            'price': current_price,
            'rsi': rsi,
            'score': score,
            'reasons': reasons
        })

    except:
        pass

results.sort(key=lambda x: x['score'], reverse=True)

message = '🏆 تحلیل بازار امین\\n\\n'

if results:
    top = results[0]
    message += (
        f'🔥 بهترین فرصت فعلی: {top["name"]}\\n'
        f'⭐ امتیاز: {top["score"]}/10\\n\\n'
    )

for coin in results[:5]:

    if coin['score'] >= 7:
        status = '🟢 بررسی خرید'
    elif coin['score'] >= 4:
        status = '🟡 تحت نظر'
    else:
        status = '🔴 فعلاً خیر'

    message += (
        f'{coin["name"]} | ⭐ {coin["score"]}/10\\n'
        f'💰 {coin["price"]:.2f}\\n'
        f'📊 RSI: {coin["rsi"]:.1f}\\n'
        f'وضعیت: {status}\\n'
    )

    if coin['reasons']:
        message += 'دلایل: ' + ' | '.join(coin['reasons']) + '\\n'

    message += '\\n'

message += '⏱ بروزرسانی: همین الان'

await update.message.reply_text(message)

------------------ اجرای ربات ------------------

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('ping', ping))
app.add_handler(CommandHandler('price', price))
app.add_handler(CommandHandler('scan', scan))

app.run_polling()
