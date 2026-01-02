from fastapi import APIRouter
from application.app_manager import manager
from api.state import contexts

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/{dataset_id}/summary")
def dataset_summary(dataset_id: int):
    ctx = contexts[dataset_id]
    summary = manager.dataset_summary_uc.execute(ctx)
    return {"summary": summary}

@router.get("/{dataset_id}/analysis")
def basic_analysis(dataset_id: int):
    ctx = contexts[dataset_id]
    analysis = manager.basic_analysis_uc.execute(ctx)
    return {"analysis": analysis}