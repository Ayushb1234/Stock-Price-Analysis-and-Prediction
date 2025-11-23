import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import accuracy_score, precision_score
import lightgbm as lgb
from db import engine

def load_feature_table(symbol):
    q = f"SELECT * FROM prices WHERE symbol='{symbol}' ORDER BY ts"
    df = pd.read_sql(q, engine)
    df = df.sort_values('ts').reset_index(drop=True)
    return df

def prepare_ml_df(df):
    # simple features using closing price
    df['return_1'] = df['close'].pct_change()
    df['ma_5'] = df['close'].rolling(5).mean()
    df['ma_20'] = df['close'].rolling(20).mean()
    df['rsi_14'] = df['close'].rolling(14).apply(lambda x: (x.diff().gt(0).sum())/len(x))  # placeholder
    df = df.dropna().reset_index(drop=True)
    # target: next-day return
    df['future_ret_1d'] = df['close'].shift(-1)/df['close'] - 1
    df = df.dropna()
    df['y'] = (df['future_ret_1d'] > 0.005).astype(int)  # 0.5% threshold
    return df

def train_symbol(symbol):
    df = load_feature_table(symbol)
    df = prepare_ml_df(df)
    X = df[['return_1','ma_5','ma_20','rsi_14']].values
    y = df['y'].values
    # time-series CV
    tscv = TimeSeriesSplit(n_splits=5)
    models=[]
    for train_idx, test_idx in tscv.split(X):
        Xtr, Xte = X[train_idx], X[test_idx]
        ytr, yte = y[train_idx], y[test_idx]
        lgbm = lgb.LGBMClassifier(n_estimators=200)
        lgbm.fit(Xtr, ytr)
        preds = lgbm.predict(Xte)
        print("acc", accuracy_score(yte, preds), "prec", precision_score(yte, preds, zero_division=0))
        models.append(lgbm)
    # save final model (retrain on full data)
    final = lgb.LGBMClassifier(n_estimators=300)
    final.fit(X, y)
    joblib.dump(final, f"models/{symbol}_lgbm.pkl")
    print("model saved for", symbol)

if __name__ == "__main__":
    import os
    os.makedirs("models", exist_ok=True)
    for sym in ["AAPL","MSFT","GOOGL"]:
        train_symbol(sym)
