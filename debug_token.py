import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "finance_dashboard_secret_key_2024"
ALGORITHM = "HS256"

expire = datetime.now(timezone.utc) + timedelta(minutes=60)
token = jwt.encode(
    {"sub": "admin@finance.com", "exp": int(expire.timestamp())},
    SECRET_KEY,
    algorithm=ALGORITHM
)
print("Token:", token)

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("Success:", payload)
except Exception as e:
    print("Error:", e)