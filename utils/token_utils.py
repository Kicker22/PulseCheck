import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")  

def generate_signed_feedback_url(encounter_id: str, base_url = "http://localhost:8000/static/index.html"):
    expiration = int((datetime.now(tz=timezone.utc) + timedelta(days=3)).timestamp())

    payload = {
        "encounter_id": encounter_id,
        "exp": expiration
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return f"{base_url}?token={token}"
