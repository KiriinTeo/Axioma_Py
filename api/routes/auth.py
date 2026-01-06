from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.app_manager import manager
from api.dependencies.db import get_db
from auth.schemas import RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    user = manager.register_user_uc.execute(
        email=req.email,
        password=req.password,
        db=db
    )
    # return {"id": user.id, "email": user.email}
    return {"user_id": user.id} # retorno simplificado por enquanto

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    return manager.login_user_uc.execute(
        email=req.email,
        password=req.password,
        db=db
    )
