from fastapi import APIRouter, Depends
from application.app_manager import manager
from api.state import contexts
from auth.dependencies import get_current_user
from api.dependencies.db import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/dataset", tags=["Dataset"])

@router.post("/load")
def load_dataset(path: str, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = user["sub"]
    ctx = manager.load_dataset_uc.execute(path, user_id, db)
    contexts[(user_id, ctx.dataset_id)] = ctx
    return {"dataset_id": ctx.dataset_id}

@router.get("/{dataset_id}/columns")
def list_columns(dataset_id: int, user: dict = Depends(get_current_user)):
    user_id = user["sub"]
    ctx = contexts[(user_id, dataset_id)]
    return manager.list_columns_uc.execute(ctx)
