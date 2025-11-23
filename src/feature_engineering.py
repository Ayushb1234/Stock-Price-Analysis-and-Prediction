import pandas as pd
import ta  # pip install ta
import json
from db import engine

def create_features(df):
    # df: sorted by ts ascending, close/open numeric
    df['return_1'] = df['close'].pct_change()
    df['ma_5'] = df['close'].rolling(window=5).mean()
    df['ma_20'] = df['close'].rolling(window=20).mean()
    df['rsi_14'] = ta.momentum.rsi(df['close'], window=14)
    df['vol_10'] = df['return_1'].rolling(10).std()
    df = df.dropna()
    return df

def export_features_to_db(symbol, df):
    # pack features into json to minimize schema churn
    rows=[]
    for _, r in df.iterrows():
        rows.append({
            "symbol": symbol,
            "ts": r['ts'],
            "feature_json": json.dumps({
                "ma_5": r['ma_5'], "ma_20": r['ma_20'], "rsi_14": r['rsi_14'], "vol_10": r['vol_10'], "return_1": r['return_1']
            }),
            "target": None,
            "model_label": None
        })
    df_out = pd.DataFrame(rows)
    df_out.to_sql('ml_features', engine, if_exists='append', index=False)

if __name__ == "__main__":
    # example: load 1 symbol, create features and write back (implement read by symbol)
    pass
