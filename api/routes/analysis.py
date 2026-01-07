from fastapi import APIRouter, Depends, HTTPException
from application.app_manager import manager
from api.state import contexts
from auth.dependencies import get_current_user

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/{dataset_id}/summary")
def dataset_summary(dataset_id: str, user=Depends(get_current_user)):
    user_id = int(user["sub"]) 

    key = (user_id, dataset_id)
    if key not in contexts:
        raise HTTPException(status_code=404, detail="Dataset não encontrado na memória.")
    
    ctx = contexts[key]
    summary = ctx.dataframe.describe()

    return {"summary": summary.to_dict()}

@router.get("/{dataset_id}/analysis")
def basic_analysis(dataset_id: str, user=Depends(get_current_user)):
    user_id = int(user["sub"])
    ctx = contexts[(user_id, dataset_id)]
    analysis = manager.basic_analysis_uc.execute(ctx)
    return {"analysis": analysis}