from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from application.app_manager import manager
from api.state import contexts
from auth.dependencies import get_current_user
from api.dependencies.deps import get_db
from infra.database.models.export import ExportModel
from uuid import uuid4

router = APIRouter(prefix="/export", tags=["Export"])

@router.post("/to_csv")
def export_dataset(dataset_id: str, path: str, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = int(user["sub"])
    
    key = (user_id, dataset_id)
    if key not in contexts:
        raise HTTPException(status_code=404, detail="Dataset não encontrado na memória.")
    
    ctx = contexts[key]
    manager.export_dataset_uc.execute(ctx, path)
    
    export_model = ExportModel(
        id=str(uuid4()),
        user_id=user_id,
        dataset_id=dataset_id,
        file_path=path,
        file_format="csv"
    )
    db.add(export_model)
    db.commit()

    return {"status": "exported", "path": path}