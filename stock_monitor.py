import os
import yfinance as yf
import requests

# Load secrets from environment (GitHub Actions)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TICKERS = os.getenv("TICKERS", "TSLA,NVDA").split(",")
REPORT_MODE = os.getenv("REPORT_MODE", "telegram")

def send_telegram_message(message: str):
    """Send message to Telegram chat via bot"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Telegram message sent successfully!")
    except Exception as e:
        print("❌ Telegram send failed:", e)

def get_stock_summary(ticker):
    """Fetch latest price info from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get("regularMarketPrice")
        change = info.get("regularMarketChangePercent")
        return f"{ticker}: ${price:.2f} ({change:+.2f}%)"
    except Exception as e:
        return f"{ticker}: Error fetching data ({e})"

def main():
    print("📈 Fetching stock data...")
    summary_lines = [get_stock_summary(t.strip()) for t in TICKERS]
    report = "🧾 *Stock Monitor Report*\n\n" + "\n".join(summary_lines)
    print(report)
    if REPORT_MODE == "telegram":
        send_telegram_message(report)

if __name__ == "__main__":
    main()
