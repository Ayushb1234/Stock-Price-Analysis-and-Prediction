from sqlalchemy import create_engine, text
from config import DB_URI

schema_sql = """
CREATE TABLE IF NOT EXISTS prices (
  id serial PRIMARY KEY,
  symbol varchar(20),
  ts timestamptz,
  open numeric,
  high numeric,
  low numeric,
  close numeric,
  volume bigint,
  source varchar(50)
);

CREATE TABLE IF NOT EXISTS ml_features (
  id serial PRIMARY KEY,
  symbol varchar(20),
  ts timestamptz,
  feature_json jsonb,
  target numeric,
  model_label varchar(20)
);

CREATE TABLE IF NOT EXISTS realtime_signals (
  id serial PRIMARY KEY,
  symbol varchar(20),
  ts timestamptz,
  last_price numeric,
  prob_up numeric,
  label varchar(20),
  expected_return numeric,
  model_name varchar(50)
);
"""

if __name__ == "__main__":
    engine = create_engine(DB_URI)
    with engine.connect() as conn:
        conn.execute(text(schema_sql))
        conn.commit()
    print("✅ Tables created successfully")
