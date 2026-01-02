from fastapi import APIRouter, HTTPException
from auth.schemas import LoginRequest, TokenResponse
from auth.security import verify_password
from auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# mock temporário (depois vira DB)
fake_user = {
    "id": "123",
    "email": "admin@axioma.com",
    "hashed_password": "$2b$12$...",  # senha já em hash
}

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    if req.email != fake_user["email"]:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if not verify_password(req.password, fake_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token({"sub": fake_user["id"], "email": fake_user["email"]})
    return {"access_token": token}
