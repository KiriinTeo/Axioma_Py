from fastapi import APIRouter, Depends
from application.app_manager import manager
from api.state import contexts
from api.schemas.loginReq import LoginRequest
from auth.dependencies import get_current_user
from api.dependencies.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    token = manager.login_user_uc.execute(
        req.email,
        req.password,
        db
    )
    return {"access_token": token}
