from jose import jwt
from uuid import uuid4
from datetime import datetime, timedelta
from .config import JWT_SECRET_KEY, JWT_EXPIRY_SECONDS

def generate_client_credentials():
    return str(uuid4()), str(uuid4())

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=JWT_EXPIRY_SECONDS)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return token, int(expire.timestamp())