from fastapi import APIRouter, Depends, HTTPException
from api.schemas.filterReq import FilterRequest
from application.app_manager import manager
from api.state import contexts  
from auth.dependencies import get_current_user
from uuid import uuid4

router = APIRouter(prefix="/filter", tags=["Filter"])  

@router.post("/apply")
def apply_filter(req: FilterRequest, user: dict = Depends(get_current_user)):
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

    return {"dataset_id": new_id}
