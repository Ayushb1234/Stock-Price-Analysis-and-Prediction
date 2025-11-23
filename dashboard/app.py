# dashboard/app.py
import streamlit as st
import sys, os, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from src.predict_realtime import predict_live
from src.insights import fetch_and_prepare, add_indicators, quick_insights

st.set_page_config(page_title="Live AI Stock Predictor", layout="wide")
st.title("📈 Live AI Stock Predictor — Charts & Insights")

# UI controls
symbols = ["AAPL", "MSFT", "GOOGL"]
symbol = st.sidebar.selectbox("Symbol", symbols)
days = st.sidebar.slider("Days back (for chart)", 30, 3650, 365)
show_indicators = st.sidebar.checkbox("Show indicators (SMA/EMA/RSI/MACD)", True)
run_pred = st.sidebar.button("Run model prediction")

# small helper: get data from DB (or fallback to yfinance)
@st.cache_data(ttl=60)
def load_prices(symbol, days):
    import sqlalchemy
    from sqlalchemy import create_engine
    import pandas as pd
    from datetime import datetime, timedelta

    # read DB URL from env or config, fallback to yfinance if DB fails
    db_url = os.environ.get("DATABASE_URL", "")
    since = (pd.Timestamp.utcnow() - pd.Timedelta(days=days)).strftime("%Y-%m-%d")
    # try DB
    if db_url:
        try:
            engine = create_engine(db_url)
            q = f"SELECT ts, open, high, low, close, volume FROM prices WHERE symbol='{symbol}' AND ts >= '{since}' ORDER BY ts"
            df = pd.read_sql_query(q, engine, parse_dates=["ts"])
            if not df.empty:
                df = df.set_index("ts")
                return df
        except Exception as e:
            # fallback to yfinance below
            st.debug(f"DB load failed: {e}")
    # fallback: yfinance
    import yfinance as yf
    df = yf.download(symbol, period=f"{days}d", interval="1d")
    if df.empty:
        return None
    df = df.rename(columns={"Adj Close":"close"})
    df = df[['Open','High','Low','Close','Volume']].rename(columns={"Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"})
    df.index.name = "ts"
    return df

df = load_prices(symbol, days)
if df is None or df.empty:
    st.warning("No price data available for this symbol/timeframe.")
    st.stop()

df = fetch_and_prepare(df)
df = add_indicators(df)

# Layout: left chart, right KPIs and insights
left, right = st.columns([3,1])

with left:
    # Candlestick
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df.index, open=df['open'], high=df['high'], low=df['low'], close=df['close'],
        name="price"))
    if show_indicators:
        if 'sma_10' in df: fig.add_trace(go.Scatter(x=df.index, y=df['sma_10'], name='SMA10', line=dict(width=1)))
        if 'sma_50' in df: fig.add_trace(go.Scatter(x=df.index, y=df['sma_50'], name='SMA50', line=dict(width=1)))
        if 'ema_20' in df: fig.add_trace(go.Scatter(x=df.index, y=df['ema_20'], name='EMA20', line=dict(width=1, dash='dot')))
    fig.update_layout(height=600, margin=dict(t=40,b=10))
    st.plotly_chart(fig, use_container_width=True)

    # Volume bar
    fig2 = px.bar(x=df.index, y=df['volume'], labels={'x':'Date','y':'Volume'}, title="Volume")
    st.plotly_chart(fig2, use_container_width=True)

    # RSI chart
    if show_indicators and 'rsi' in df:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df.index, y=df['rsi'], name='RSI'))
        fig3.update_layout(height=250, yaxis=dict(range=[0,100]), margin=dict(t=20,b=10))
        st.plotly_chart(fig3, use_container_width=True)

with right:
    st.header("Quick KPIs")
    last = df.iloc[-1]
    st.metric("Price", f"${last['close']:.2f}")
    st.metric("Change", f"{(last['close']-df.iloc[-2]['close']):+.2f} ({(last['close']/df.iloc[-2]['close']-1)*100:+.2f}%)")
    st.metric("Volume", f"{int(last['volume']):,}")

    st.markdown("---")
    st.header("Insights")
    insights = quick_insights(df)
    for s in insights:
        st.write(f"- {s}")

    st.markdown("---")
    if run_pred:
        with st.spinner("Running model..."):
            action, confidence = predict_live(symbol)
            if action is None:
                st.error("Model or live data not available.")
            else:
                st.success(f"Model says: **{action}**")
                st.write(f"Confidence: {confidence*100:.2f}%")

# feature importance: try to show model importance if model exists
import joblib, pathlib
model_file = pathlib.Path(__file__).parents[1] / "models" / f"{symbol}.pkl"
if model_file.exists():
    try:
        model = joblib.load(str(model_file))
        # try LightGBM booster or sklearn estimator with feature_importances_
        import numpy as np
        if hasattr(model, "feature_importances_"):
            fi = model.feature_importances_
            features = ["close", "volume", "high", "low"]  # adjust if different
            fig_fi = px.bar(x=features, y=fi, labels={'x':'feature','y':'importance'}, title="Feature importance")
            st.plotly_chart(fig_fi, use_container_width=True)
    except Exception as e:
        st.write("Could not load model for feature importance.")
