from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.dependencies.deps import get_db

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("")
def healthcheck(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1 FROM DUAL"))
    except Exception:
        return {"status": "comprometido"}

    return {"status": "saudavel"}
