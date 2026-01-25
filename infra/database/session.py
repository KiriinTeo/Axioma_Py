from sqlalchemy.orm import sessionmaker
from infra.database.connection import engine, SessionLocal

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
