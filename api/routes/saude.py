from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies.db import get_db

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
    except Exception:
        return {"status": "comprometido"}

    return {"status": "saudavel"}
