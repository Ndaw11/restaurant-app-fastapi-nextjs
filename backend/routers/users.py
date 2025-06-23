from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserOut, UpdateRole
from utils.security import is_admin
from crud import user as crud_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.get("/users", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db), _=Depends(is_admin)):
    return crud_user.get_all_users(db)


@router.put("/users/{user_id}/role", response_model=UserOut)
def change_user_role(user_id: int,
                     data: UpdateRole,
                     db: Session = Depends(get_db),
                     _: str = Depends(is_admin)):
    user = crud_user.update_user_role(db, user_id, data.role)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user
