from sqlalchemy.orm import Session
from ..models import user as user_model
from ..schemas import user as user_schemas
from ..core import security
from fastapi import HTTPException, status

def update_user_password(db: Session, current_user: user_model.User, user_update: user_schemas.UserUpdatePassword) -> None:
        """Обновляет пароль пользователя."""
        if not security.verify_password(user_update.old_password, current_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid old password")
        hashed_password = security.get_password_hash(user_update.new_password)
        current_user.hashed_password = hashed_password
        db.commit()
        db.refresh(current_user)