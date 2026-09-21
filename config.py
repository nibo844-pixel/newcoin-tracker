import os
def _load_dotenv():
    try:
        with open(".env") as f:
            for line in f.read().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    except FileNotFoundError:
        pass
_load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ALERT_CHAT_ID = os.environ.get("ALERT_CHAT_ID", "")
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", "300"))
REQUIRE_TELEGRAM = os.environ.get("REQUIRE_TELEGRAM", "1") == "1"
REQUIRE_X = os.environ.get("REQUIRE_X", "1") == "1"
MIN_LIQUIDITY_USD = float(os.environ.get("MIN_LIQUIDITY_USD", "0"))
MIN_FDV_USD = float(os.environ.get("MIN_FDV_USD", "0"))
X_API_KEY = os.environ.get("X_API_KEY", "")
X_API_SECRET = os.environ.get("X_API_SECRET", "")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN", "")
X_ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET", "")
DB_PATH = os.environ.get("DB_PATH", "data/seen.db")
