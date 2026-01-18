from infra.database.session import get_sessionmaker

def get_db():
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
