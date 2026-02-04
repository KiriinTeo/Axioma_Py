from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings
import os

def get_engine():
    if settings.ORACLE_DSN and settings.ORACLE_USER and settings.ORACLE_PASSWORD:
        url = (
            f"oracle+oracledb://{settings.ORACLE_USER}:"
            f"{settings.ORACLE_PASSWORD}@{settings.ORACLE_DSN}"
        )
        
        wallet_dir = os.path.abspath(settings.TNS_ADMIN) if settings.TNS_ADMIN else None
        
        connect_args = {
            "config_dir": wallet_dir,
            "wallet_location": wallet_dir,
        }
        
        if settings.WALLET_PASSWORD:
            connect_args["wallet_password"] = settings.WALLET_PASSWORD
        
        return create_engine(
            url,
            connect_args=connect_args,
            echo=settings.DEBUG,
            pool_pre_ping=True,
            pool_recycle=3600  
        )
    
    db_url = settings.DATABASE_URL or "sqlite:///./test.db"
    return create_engine(
        db_url,
        echo=settings.DEBUG,
        connect_args={"check_same_thread": False}
    )

engine = get_engine()
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
