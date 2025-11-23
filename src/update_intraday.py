# polling intraday via Finnhub REST (simple)
import requests, time, pandas as pd
from config import FINNHUB_API_KEY
from db import write_prices

def fetch_quote(symbol):
    url = "https://finnhub.io/api/v1/quote"
    r = requests.get(url, params={"symbol":symbol, "token": FINNHUB_API_KEY})
    return r.json()

def poll_symbols(symbols):
    rows=[]
    for s in symbols:
        q = fetch_quote(s)
        # q contains c (current), h, l, o, pc
        rows.append({
            "symbol": s,
            "ts": pd.Timestamp.utcnow(),
            "open": q.get("o"),
            "high": q.get("h"),
            "low": q.get("l"),
            "close": q.get("c"),
            "volume": None,
            "source": "finnhub_quote"
        })
    df = pd.DataFrame(rows)
    write_prices(df)

if __name__ == "__main__":
    symbols = ["AAPL","MSFT","GOOGL"]
    while True:
        poll_symbols(symbols)
        time.sleep(60)  # every 60s or as allowed by your plan; Finnhub has websocket option for tighter realtime. :contentReference[oaicite:3]{index=3}
