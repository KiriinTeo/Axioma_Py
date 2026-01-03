class LoginUserUseCase:
    def __init__(self, user_repo, password_service, token_service):
        self.user_repo = user_repo
        self.password_service = password_service
        self.token_service = token_service

    def execute(self, email: str, password: str, db):
        user = self.user_repo.get_by_email(email, db)

        if not user:
            raise ValueError("Credenciais inválidas")

        if not self.password_service.verify(password, user.hashed_password):
            raise ValueError("Credenciais inválidas")

        return self.token_service.create({
            "sub": user.id,
            "email": user.email
        })
