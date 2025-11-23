# src/insights.py
import pandas as pd
import numpy as np
import ta  # pip install ta

def fetch_and_prepare(df):
    """
    Normalize dataframe:
    - ensure datetime index
    - flatten multiindex columns if present
    - lowercase/rename common columns to: open, high, low, close, volume
    - ensure each of those is a 1-D numeric Series
    """
    df = df.copy()

    # make sure index is datetime
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        try:
            df.index = pd.to_datetime(df.index)
        except Exception:
            # try column 'ts'
            if 'ts' in df.columns:
                df['ts'] = pd.to_datetime(df['ts'])
                df = df.set_index('ts')

    df = df.sort_index()

    # Flatten MultiIndex columns if any
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join([str(x) for x in col if x is not None and str(x) != '']) for col in df.columns]

    # normalize column names to lowercase
    df.columns = [c.lower().strip() for c in df.columns]

    # common rename
    col_map = {}
    if 'adj close' in df.columns:
        col_map['adj close'] = 'close'
    if 'close' in df.columns:
        col_map.setdefault('close', 'close')
    if 'open' in df.columns:
        col_map.setdefault('open', 'open')
    if 'high' in df.columns:
        col_map.setdefault('high', 'high')
    if 'low' in df.columns:
        col_map.setdefault('low', 'low')
    if 'volume' in df.columns:
        col_map.setdefault('volume', 'volume')
    if col_map:
        df = df.rename(columns=col_map)

    # if columns are like "('close','AAPL')" after earlier ops, try to detect substring close
    for needed in ['open','high','low','close','volume']:
        if needed not in df.columns:
            # try to find column that contains the word
            for col in df.columns:
                if needed in col:
                    df = df.rename(columns={col: needed})
                    break

    # ensure each target column is 1D numeric Series
    for col in ['open','high','low','close','volume']:
        if col in df.columns:
            # if column is DataFrame (e.g. df[col] yields a DF), squeeze to Series
            series = df[col]
            if isinstance(series, pd.DataFrame):
                # take first column if it's single-col DataFrame
                series = series.iloc[:, 0]
            # coerce to numeric
            df[col] = pd.to_numeric(series, errors='coerce')

    return df

def add_indicators(df):
    """
    Add technical indicators. Expects df with 1-D numeric 'close' series.
    """
    df = df.copy()

    # defensive check: ensure close is 1-D Series
    if 'close' not in df.columns:
        raise ValueError("DataFrame must contain a 'close' column after fetch_and_prepare()")

    # If df['close'] somehow a DataFrame, squeeze it
    if isinstance(df['close'], pd.DataFrame):
        df['close'] = df['close'].iloc[:, 0]

    # ensure numeric dtype
    df['close'] = pd.to_numeric(df['close'], errors='coerce')

    # basic moving averages
    df['sma_10'] = df['close'].rolling(10, min_periods=1).mean()
    df['sma_50'] = df['close'].rolling(50, min_periods=1).mean()
    df['ema_20'] = df['close'].ewm(span=20, adjust=False).mean()

    # RSI (14) - ta expects a 1D array/Series
    # make sure to pass series (not a numpy 2D)
    close_series = df['close'].astype(float).dropna()
    if len(close_series) >= 1:
        # compute RSI and reindex to original df index (so lengths match)
        rsi_obj = ta.momentum.RSIIndicator(close=close_series, window=14)
        rsi_series = rsi_obj.rsi()
        # reindex to original index (NaN where not available)
        df['rsi'] = rsi_series.reindex(df.index)
    else:
        df['rsi'] = np.nan

    # MACD
    macd_obj = ta.trend.MACD(close=df['close'].fillna(method='ffill'), window_slow=26, window_fast=12, window_sign=9)
    df['macd'] = macd_obj.macd()
    df['macd_signal'] = macd_obj.macd_signal()

    # volatility (20-day std of returns)
    df['volatility_20'] = df['close'].pct_change().rolling(20).std()

    return df

def quick_insights(df):
    """Return short human-friendly insights string list"""
    out = []
    if df is None or len(df) < 2:
        return ["No data available"]
    last = df.iloc[-1]
    prev = df.iloc[-2]

    # trend
    if pd.notna(last.get('sma_50')) and last['close'] > last.get('sma_50', last['close']):
        out.append("📈 Price above 50-day SMA (bullish bias)")
    else:
        out.append("📉 Price below 50-day SMA (bearish bias)")

    # cross
    if pd.notna(last.get('sma_10')) and pd.notna(last.get('sma_50')):
        if last['sma_10'] > last['sma_50'] and df.iloc[-2]['sma_10'] <= df.iloc[-2]['sma_50']:
            out.append("✨ Bullish crossover: 10-day SMA crossed above 50-day SMA")
        elif last['sma_10'] < last['sma_50'] and df.iloc[-2]['sma_10'] >= df.iloc[-2]['sma_50']:
            out.append("⚠️ Bearish crossover: 10-day SMA crossed below 50-day SMA")

    # RSI
    if pd.notna(last.get('rsi')):
        if last['rsi'] > 70:
            out.append("🔴 RSI > 70 — overbought")
        elif last['rsi'] < 30:
            out.append("🟢 RSI < 30 — oversold")
        else:
            out.append(f"RSI: {last['rsi']:.1f}")
    else:
        out.append("RSI: n/a")

    # volatility spike
    vol = last.get('volatility_20', 0)
    if vol and vol > df['volatility_20'].mean() * 1.8:
        out.append("⚡ Volatility spike detected (big move)")

    # momentum / immediate change
    try:
        pct = (last['close'] - prev['close']) / prev['close'] * 100
        out.append(f"Last change: {pct:.2f}%")
    except Exception:
        out.append("Last change: n/a")

    return out
