from fastapi import APIRouter
from application.app_manager import manager
from api.state import contexts

router = APIRouter(prefix="/dataset", tags=["Dataset"])

@router.post("/load")
def load_dataset(path: str):
    ctx = manager.load_dataset_uc.execute(path)
    ctx_id = id(ctx)
    contexts[ctx_id] = ctx
    return {"dataset_id": ctx_id}

@router.get("/{dataset_id}/columns")
def list_columns(dataset_id: int):
    ctx = contexts[dataset_id]
    return manager.list_columns_uc.execute(ctx)
