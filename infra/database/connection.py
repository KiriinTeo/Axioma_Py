from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings

def get_engine():
    if settings.ENV == "production" and settings.ORACLE_DSN:
        url = (
            f"oracle+oracledb://{settings.ORACLE_USER}:"
            f"{settings.ORACLE_PASSWORD}@{settings.ORACLE_DSN}"
        )

        return create_engine(
            url,
            echo=settings.DEBUG,
            pool_pre_ping=True
        )

    return create_engine(
        settings.database_url,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False}
    )

engine = get_engine()
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
