from fastapi import APIRouter, Depends
from application.app_manager import manager
from api.state import contexts
from auth.dependencies import get_current_user

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/{dataset_id}/summary")
def dataset_summary(dataset_id: int, user=Depends(get_current_user)): # adicionando exemplo de autenticação com base nas doc, revisitar depois
    user_id = user["sub"]
    ctx = contexts[(user_id, dataset_id)]
    summary = manager.dataset_summary_uc.execute(ctx)
    return {"summary": summary}

@router.get("/{dataset_id}/analysis")
def basic_analysis(dataset_id: int, user=Depends(get_current_user)):
    user_id = user["sub"]
    ctx = contexts[(user_id, dataset_id)]
    analysis = manager.basic_analysis_uc.execute(ctx)
    return {"analysis": analysis}