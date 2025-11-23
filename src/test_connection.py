from sqlalchemy import create_engine
from config import DB_URI

try:
    engine = create_engine(DB_URI)
    engine.connect()
    print("🔥 Connected successfully to PostgreSQL!")
except Exception as e:
    print("❌ Connection failed:", e)
