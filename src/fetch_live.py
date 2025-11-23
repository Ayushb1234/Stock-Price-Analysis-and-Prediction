import yfinance as yf
import pandas as pd

def get_live_data(symbol):
    df = yf.download(symbol, period="1d", interval="1m")
    if df.empty:
        return None
    df = df.tail(1).reset_index()
    df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    }, inplace=True)
    return df
