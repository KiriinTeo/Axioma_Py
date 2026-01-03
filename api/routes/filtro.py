from fastapi import APIRouter, Depends
from api.schemas.filter import FilterRequest
from application.app_manager import manager
from api.state import contexts  
from auth.dependencies import get_current_user

router = APIRouter(prefix="/filter", tags=["Filter"])  

@router.post("/apply")
def apply_filter(req: FilterRequest, user: dict = Depends(get_current_user)):
    user_id = user["sub"]
    ctx = contexts[req.dataset_id]

    new_ctx = manager.apply_filter_uc.execute(
        ctx=ctx,
        column=req.column,
        operator=req.operator,
        value=req.value
    )

    new_id = id(new_ctx)
    contexts[(user_id, new_id)] = new_ctx

    return {"dataset_id": new_id}
