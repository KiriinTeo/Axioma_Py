from fastapi import APIRouter
from application.app_manager import manager
from api.state import contexts

router = APIRouter(prefix="/export", tags=["Export"])

@router.post("/to_csv")
def export_dataset(dataset_id: int, path: str):
    ctx = contexts[dataset_id]
    manager.export_dataset_uc.execute(ctx, path)
    return {"status": "exported", "path": path}