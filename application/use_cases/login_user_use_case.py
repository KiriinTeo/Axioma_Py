from auth.security import verify_password
from auth.jwt import create_access_token
from fastapi import HTTPException
from infra.database.repositories.user_repo import UserRepository as user_repo

class LoginUserUseCase:
    def execute(self, email: str, password: str, db):
        user = user_repo(db).get_by_email(email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": str(user.id)})
        return {
            "access_token": token,
            "token_type": "bearer"
        }

