from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import user as user_schemas
from ..services import user as user_service
from ..services import auth as auth_service
from ..core.database import get_db
from ..utils.logger import logger

router = APIRouter()

@router.patch("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user_update: user_schemas.UserUpdatePassword,
                          db: Session = Depends(get_db),
                          token: str = Depends(auth_service.get_current_user_by_token)):
    """Изменяет пароль текущего пользователя."""
    try:
        logger.info(f"Attempting password change for user: {token.id}")
        user_service.update_user_password(db, token, user_update)
        logger.info(f"User {token.id} changed password successfully")
    except Exception as e:
        logger.error(f"Error password change for user: {token.id}. Error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))