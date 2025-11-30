# 📈 Real-Time AI Stock Predictor (ML + Streamlit Dashboard)

An **AI-powered real-time stock analysis system** built using:

- 🧠 Machine Learning (LightGBM)
- 📊 Interactive Dashboard (Streamlit + Plotly)
- 💹 Live market data feed (Yahoo Finance API)
- 🗂 PostgreSQL / Local mode fallback
- 🔁 Automated prediction pipeline

This project predicts **BUY / SELL signals** with confidence scores and displays:

✔ Candlestick charts  
✔ Volume trends  
✔ Technical indicators (RSI, MACD, SMA, EMA)  
✔ Feature importance  
✔ Auto-generated human insights  

---

## 🚀 Features

| Feature | Status |
|--------|--------|
| Real-time market data fetch | ✅ |
| Model prediction (Buy/Sell + confidence) | ✅ |
| ML Models stored for each stock | ✅ |
| Interactive charts (candles, volume, RSI, MACD) | ✅ |
| Technical analysis insights | ✅ |
| Refresh + live update | ✅ |
| Deployable to Streamlit Cloud | ✅ |

---

## 🏗 Project Structure

```bash
stock-rt-powerbi-ml/
│
├─ dashboard/
│  └─ app.py                    # Streamlit UI
│
├─ src/
│  ├─ predict_realtime.py       # Load model + run live predictions
│  ├─ fetch_live.py             # Fetch latest price from Yahoo Finance
│  ├─ insights.py               # Technical indicators + insights generator
│  ├─ train_model.py            # Model training script (LightGBM)
│  └─ download_historical.py    # Historical data downloader
│
├─ models/                      # Saved ML models (AAPL.pkl, MSFT.pkl…)
├─ data/                        # Optional seed data
├─ requirements.txt
└─ README.md
```
 
Deployment Link : https://stock-price-analysis-and-prediction-qsnxiuus2ysweyidepeb9c.streamlit.app/


