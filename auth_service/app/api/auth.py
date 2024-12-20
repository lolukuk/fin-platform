from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import user as user_schemas
from ..services import auth as auth_service
from ..core.database import get_db
from ..core.security import create_jwt_token
from ..utils.logger import logger

router = APIRouter()

@router.post("/register", response_model=user_schemas.User)
async def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """Регистрирует нового пользователя."""
    try:
        db_user = auth_service.create_user(db, user)
        logger.info(f"User {db_user.id} registered successfully")
        return db_user
    except Exception as e:
         logger.error(f"Error registration user. Error: {e}")
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

@router.post("/login", response_model=user_schemas.Token)
async def login_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """Аутентифицирует пользователя и возвращает JWT-токен."""
    logger.info(f"Attempting login for user: {user.username}")
    token = auth_service.authenticate_user(db, user.username, user.password)
    logger.info(f"User {user.username} logged in successfully")
    return token