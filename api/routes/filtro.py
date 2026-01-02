from fastapi import APIRouter
from api.schemas.filter import FilterRequest
from application.app_manager import manager
from api.state import contexts  

router = APIRouter(prefix="/filter", tags=["Filter"])  

@router.post("/apply")
def apply_filter(req: FilterRequest):
    ctx = contexts[req.dataset_id]

    new_ctx = manager.apply_filter_uc.execute(
        ctx=ctx,
        column=req.column,
        operator=req.operator,
        value=req.value
    )

    new_id = id(new_ctx)
    contexts[new_id] = new_ctx

    return {"dataset_id": new_id}
