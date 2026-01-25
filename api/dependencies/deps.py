from infra.database.connection import SessionLocal

# Dependency injection para pegar a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
