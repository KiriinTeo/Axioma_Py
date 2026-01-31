from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from application.app_manager import manager
from api.dependencies.deps import get_db
from auth.schemas import RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    user = manager.register_user_uc.execute(
        email=req.email,
        password=req.password,
        id=req.id,
        db=db
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"user_id": user.id} # retorno simplificado por enquanto

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    login = manager.login_user_uc.execute(
        email=req.email,
        password=req.password,
        db=db
    )
    """ db.add(login)
    db.commit()
    db.refresh(login) """

    return login
    
