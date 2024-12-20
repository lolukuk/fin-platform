from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Dict
import jwt
from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Хеширует пароль."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет хешированный пароль."""
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: Dict, expires_delta: timedelta | None = None) -> str:
    """Генерирует JWT-токен."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def decode_jwt_token(token: str) -> Dict:
    """Декодирует JWT-токен."""
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])