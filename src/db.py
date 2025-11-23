from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from config import DB_URI
import pandas as pd

engine = create_engine(DB_URI, pool_pre_ping=True)

def write_prices(df, table="prices"):
    # df must have: symbol, ts (ISO string), open, high, low, close, volume
    df.to_sql(table, engine, if_exists="append", index=False, method='multi', chunksize=1000)

def read_prices(symbol, limit_days=365):
    q = text("""
        SELECT * FROM prices
        WHERE symbol = :sym
        ORDER BY ts DESC
        LIMIT :limit
    """)
    return pd.read_sql(q.bindparams(sym=symbol, limit=limit_days*24*60), engine)
