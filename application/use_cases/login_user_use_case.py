from auth.security import verify_password
from auth.jwt import create_access_token
from infra.database.models.user import UserModel as User
from fastapi import HTTPException

class LoginUserUseCase:
    def execute(self, email: str, password: str, db):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": str(user.id)})
        return {
            "access_token": token,
            "token_type": "bearer"
        }

