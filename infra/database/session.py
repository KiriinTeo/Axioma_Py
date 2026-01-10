from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings

#DATABASE_URL = "sqlite:///./axioma.db"
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
