from fastapi import APIRouter, Depends
from application.app_manager import manager
from api.state import contexts
from auth.dependencies import get_current_user

router = APIRouter(prefix="/export", tags=["Export"])

@router.post("/to_csv")
def export_dataset(dataset_id: str, path: str, user: dict = Depends(get_current_user)):
    user_id = int(user["sub"])
    ctx = contexts[(user_id, dataset_id)]
    manager.export_dataset_uc.execute(ctx, path)
    return {"status": "exported", "path": path}