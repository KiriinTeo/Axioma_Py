from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas.filterReq import FilterRequest
from application.app_manager import manager
from api.state import contexts  
from auth.dependencies import get_current_user
from api.dependencies.deps import get_db
from infra.database.models.filter import FilterModel
from uuid import uuid4

router = APIRouter(prefix="/filter", tags=["Filter"])  

@router.post("/apply")
def apply_filter(req: FilterRequest, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = int(user["sub"])
    
    key = (user_id, req.dataset_id)
    if key not in contexts:
        raise HTTPException(status_code=404, detail="Dataset não encontrado na memória.")
    
    ctx = contexts[key]

    new_ctx = manager.apply_filter_uc.execute(
        ctx=ctx,
        column=req.column,
        operator=req.operator,
        value=req.value
    )

    new_id = str(uuid4())
    contexts[(user_id, new_id)] = new_ctx
    
    filter_model = FilterModel(
        id=new_id,
        user_id=user_id,
        dataset_id=req.dataset_id,
        column_name=req.column,
        operator=req.operator,
        value=req.value
    )
    db.add(filter_model)
    db.commit()

    return {"dataset_id": new_id}
