from sqlalchemy.orm import Session
from ..models import user as user_model
from ..schemas import user as user_schemas
from ..core import security
from fastapi import HTTPException, status
from typing import Dict


def create_user(db: Session, user: user_schemas.UserCreate) -> user_model.User:
    """Создает нового пользователя."""
    hashed_password = security.get_password_hash(user.password)
    db_user = user_model.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str) -> Dict | None:
    """Аутентифицирует пользователя."""
    user = db.query(user_model.User).filter(user_model.User.username == username).first()
    if not user or not security.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token = security.create_jwt_token(data={'sub': str(user.id)})
    return {'access_token': token, 'token_type': 'bearer'}


def get_current_user_by_token(db: Session, token: str) -> user_model.User:
    """Получает текущего пользователя по токену."""
    try:
        payload = security.decode_jwt_token(token)
        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")