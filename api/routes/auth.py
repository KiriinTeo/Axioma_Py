from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from application.app_manager import manager
from api.dependencies.deps import get_db
from auth.jwt import create_access_token
from auth.schemas import RegisterRequest, LoginRequest
from infra.database.repositories import user_repo


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
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username   
    password = form_data.password
    user_rep = user_repo.UserRepository(db)

    user = user_rep.get_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
