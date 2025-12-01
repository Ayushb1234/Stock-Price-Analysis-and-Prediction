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
# Live Deployment:
-----------------
Deployment Link : https://stock-price-analysis-and-prediction-qsnxiuus2ysweyidepeb9c.streamlit.app/

# Screenshots of Project
------------------------

<img width="1819" height="925" alt="image" src="https://github.com/user-attachments/assets/0658dc12-33e5-4470-bf7b-d9ea5c3a4871" />
<img width="1764" height="940" alt="image" src="https://github.com/user-attachments/assets/4d8702aa-7dd7-4690-806c-45f0ef69c415" />

⚙️ Installation

1️⃣ Clone Repo
```
git clone https://github.com/<your-username>/stock-rt-powerbi-ml.git
cd stock-rt-powerbi-ml
```
2️⃣ Create Virtual Environment
```
python -m venv venv

```
Activate:
```
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```
3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

## 🧠 How It Works

## Stage Description
---------------------

1. Data fetching	Live stock data retrieved via Yahoo Finance
2. Feature engineering	Volume, OHLC features, technical indicators
3. Model inference	LightGBM model predicts BUY/SELL
4. Confidence scores	predict_proba() returns decision confidence
5. Visualization	Plotly + Streamlit render interactive analysis charts
6. Insights engine	Auto-text reasoning based on RSI/MACD/Crossovers

Candlestick	RSI + MACD

	
## 🔮 Future Enhancements
-----------------------------

📩 Telegram or Email trading alerts

🧩 Portfolio optimization / backtesting

🧠 Reinforcement learning model

⏱ Auto-refresh interval (5s / 15s / 30s toggle)

🌍 Multi-market (Crypto, Forex, Indian NSE/BSE)

🛠 Tech Stack
-------------
Layer	Tools
Programming	Python
Dashboard	Streamlit + Plotly
AI/ML	Scikit-learn, LightGBM
Data Source	Yahoo Finance (yfinance)
Optional DB	PostgreSQL

##🤝 Contributing
------------------

PRs are welcome. For major changes, please open an issue.

## ⭐ Support
--------------

If this project helped you — star the repo ⭐ and share it!

## Author
---------
👤 Ayush
💻 AI/ML Developer
🚀 Gen-Z Engineer who automates financial decision making.



