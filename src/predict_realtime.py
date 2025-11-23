import os
import joblib
from src.fetch_live import get_live_data


def predict_live(symbol: str):
    """Load live data + model and return BUY/SELL + confidence"""

    # 1) Fetch live price
    df = get_live_data(symbol)
    if df is None or df.empty:
        return None, None

    # 2) Build model path. (_lgbm.pkl instead of plain .pkl)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_filename = f"{symbol.upper()}_lgbm.pkl"
    model_path = os.path.join(BASE_DIR, "..", "models", model_filename)

    if not os.path.exists(model_path):
        return f"❌ Model not found for {symbol}", None

    # 3) Load trained model
    model = joblib.load(model_path)

    features = ["close", "volume", "high", "low"]
    df = df.tail(1)  # last row only (most recent)

    # 4) Predict
    prediction = model.predict(df[features])[0]
    confidence = max(model.predict_proba(df[features])[0])

    action = "BUY" if prediction == 1 else "SELL"

    return action, round(confidence, 3)
