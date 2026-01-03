class RegisterUserUseCase:
    def __init__(self, user_repo, password_service):
        self.user_repo = user_repo
        self.password_service = password_service

    def execute(self, email: str, password: str, db):
        if self.user_repo.exists(email, db):
            raise ValueError("Usuário já existe")

        hashed = self.password_service.hash(password)
        user = self.user_repo.create(email, hashed, db)
        return user.id
