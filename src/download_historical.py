# import requests
# import time
# import pandas as pd
# from config import ALPHA_VANTAGE_KEY
# from db import write_prices

# def download_daily(symbol):
#     url = "https://www.alphavantage.co/query"
#     params = {
#         "function": "TIME_SERIES_DAILY",
#         "symbol": symbol,
#         "outputsize": "compact",
#         "apikey": ALPHA_VANTAGE_KEY
#     }

#     print(f"Fetching: {symbol}")
#     r = requests.get(url, params=params)
#     data = r.json()

#     # New structure validation
#     if "Time Series (Daily)" not in data:
#         print(f"⚠️ No data returned for {symbol}. Response:")
#         print(data)
#         return

#     time_series = data["Time Series (Daily)"]

#     rows=[]
#     for date, vals in time_series.items():
#         rows.append({
#             "symbol": symbol,
#             "ts": date,
#             "open": float(vals["1. open"]),
#             "high": float(vals["2. high"]),
#             "low": float(vals["3. low"]),
#             "close": float(vals["4. close"]),
#             "volume": int(vals["5. volume"]),
#             "source": "alpha_vantage"
#         })

#     df = pd.DataFrame(rows)
#     write_prices(df)
#     print(f"✅ Inserted {len(df)} rows for {symbol}")

# if __name__ == "__main__":
#     symbols = ["AAPL", "MSFT", "GOOGL"]

#     for sym in symbols:
#         download_daily(sym)
#         time.sleep(15)  # avoid rate limit (5 requests/min)

import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from config import DB_URI

engine = create_engine(DB_URI)

def save_stock(symbol):
    print(f"Downloading {symbol}...")
    df = yf.download(symbol, start="2015-01-01")

    if df.empty:
        print(f"⚠️ No data for {symbol}")
        return

    # ---- FIX: flatten multi-index column names ----
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    # rename to match database schema
    df = df.reset_index()
    df['symbol'] = symbol
    df = df.rename(columns={
        "Date": "ts",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Adj Close": "adj_close",
        "Volume": "volume"
    })

    # Keep only expected fields
    cols = ["ts", "symbol", "open", "high", "low", "close", "volume"]
    df = df[cols]

    # ---- Insert into database ----
    df.to_sql("prices", engine, if_exists="append", index=False)
    print(f"✔ Inserted {len(df)} rows for {symbol}")

if __name__ == "__main__":
    symbols = ["AAPL", "MSFT", "GOOGL"]
    for sym in symbols:
        save_stock(sym)
