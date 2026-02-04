from auth.security import get_password_hash
from infra.database.repositories.user_repo import UserRepository as user_repo

class RegisterUserUseCase:
    def execute(self, email: str, password: str, id: int, db):
        existing = user_repo(db).get_by_email(email)

        if existing:
            raise ValueError("User already exists")

        user = user_repo(db).create(
            email=email,
            password_hash=get_password_hash(password),
            id=id
        )

        return user