from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import oracledb
from config import settings

def get_engine():
    if settings.ORACLE_DSN:
        oracledb.init_oracle_client(
            config_dir=settings.ORACLE_WALLET_PATH
        )

        url = (
            f"oracle+oracledb://{settings.ORACLE_USER}:"
            f"{settings.ORACLE_PASSWORD}@{settings.ORACLE_DSN}"
        )

        return create_engine(url, echo=settings.DEBUG)

    return create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

engine = get_engine()
SessionLocal = sessionmaker(bind=engine)
