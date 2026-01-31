from infra.database.models.user import UserModel
import random

class UserRepository:
    def __init__(self, db):
        self.db = db

    def create(self, email: str, password_hash: str, id: int) -> UserModel:
        user = UserModel(
            email=email,
            password_hash=password_hash,
            id= random.randint(1, 999999)
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> UserModel | None:
        return (
            self.db.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

    def get_by_id(self, user_id: str) -> UserModel | None:
        return self.db.query(UserModel).get(user_id)
