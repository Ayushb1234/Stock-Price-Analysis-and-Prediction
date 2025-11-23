import os
from dotenv import load_dotenv
load_dotenv()

# APIs
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY", "")

# Postgres
DB_URI = os.getenv("DB_URI", "postgresql://postgres:Ayush@localhost:5432/postgres")

# Power BI (you'll get dataset_id + push rows endpoint after creating dataset)
POWERBI_PUSH_URL = os.getenv("POWERBI_PUSH_URL", "")  # e.g., https://api.powerbi.com/beta/your_workspace/datasets/<datasetId>/tables/<tableName>/rows
POWERBI_BEARER = os.getenv("POWERBI_BEARER", "")      # Azure AD token for Power BI (bearer)

print("Alpha Key:", ALPHA_VANTAGE_KEY)  # TEMP debug
