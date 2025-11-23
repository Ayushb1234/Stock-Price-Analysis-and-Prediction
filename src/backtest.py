import pandas as pd
import joblib
from db import engine

def backtest(symbol, model_path):
    df = pd.read_sql(f"SELECT * FROM prices WHERE symbol='{symbol}' ORDER BY ts", engine)
    df = df.sort_values('ts').reset_index(drop=True)
    # create features as in training
    df['return_1'] = df['close'].pct_change()
    df['ma_5'] = df['close'].rolling(5).mean()
    df['ma_20'] = df['close'].rolling(20).mean()
    df['rsi_14'] = df['close'].rolling(14).apply(lambda x: (x.diff().gt(0).sum())/len(x))
    df = df.dropna().reset_index(drop=True)
    X = df[['return_1','ma_5','ma_20','rsi_14']].values
    model = joblib.load(model_path)
    probs = model.predict_proba(X)[:,1]
    df['prob_up'] = probs
    df['pred'] = (probs > 0.6).astype(int)  # threshold
    # simulate
    trades=[]
    equity=1.0
    for i in range(len(df)-1):
        if df.loc[i,'pred'] == 1:
            # buy at next open, sell at next close
            entry = df.loc[i+1,'open']
            exit = df.loc[i+1,'close']
            ret = (exit/entry)-1
            equity *= (1+ret)
            trades.append(ret)
    total_return = equity - 1
    import numpy as np
    cagr = (1+total_return)**(252/len(df)) - 1
    print("total_return", total_return, "CAGR approx", cagr, "trades", len(trades))
    return trades

if __name__ == "__main__":
    backtest("AAPL", "models/AAPL_lgbm.pkl")
