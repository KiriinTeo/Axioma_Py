from auth.security import get_password_hash
from infra.database.models.user import UserModel as User

class RegisterUserUseCase:
    def execute(self, email: str, password: str, db):
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            raise ValueError("User already exists")

        user = User(
            email=email,
            hashed_password=get_password_hash(password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        return user