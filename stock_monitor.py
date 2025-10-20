import yfinance as yf
from telegram import Bot
import schedule
import time

# === CONFIG ===
BOT_TOKEN = "8024607904:AAGVqnXtP7SavrJmEJ3dJg1XoZnLAaqQvDA"
CHAT_ID = "8165534401"
STOCKS = ["NVDA", "AAPL", "MSFT"]
INTERVAL_MINUTES = 60  # how often to check
ALERT_PERCENT = 2  # send message only if change >2%

bot = Bot(token=BOT_TOKEN)

# store last known prices
last_prices = {}

def get_price(ticker):
    data = yf.Ticker(ticker)
    hist = data.history(period="2d")  # last 2 days
    if len(hist) < 2:
        return None, None
    today_price = hist["Close"].iloc[-1]
    prev_price = hist["Close"].iloc[-2]
    pct_change = (today_price - prev_price) / prev_price * 100
    return round(today_price, 2), round(pct_change, 2)

def send_update():
    global last_prices
    msg_lines = []
    for t in STOCKS:
        price, pct = get_price(t)
        if price is None:
            continue
        last_pct = last_prices.get(t, None)
        # check if change exceeds threshold or first time
        if last_pct is None or abs(pct) >= ALERT_PERCENT:
            msg_lines.append(f"{t}: ${price} ({pct}%)")
            last_prices[t] = pct  # update last known change

    if msg_lines:
        msg = "📈 Stock Alert:\n" + "\n".join(msg_lines)
        bot.send_message(chat_id=CHAT_ID, text=msg)
        print("Sent alert:\n", msg)
    else:
        print("No significant changes.")

# schedule the updates
schedule.every(INTERVAL_MINUTES).minutes.do(send_update)

print("Bot running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(5)
