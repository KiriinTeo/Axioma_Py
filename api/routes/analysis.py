from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from application.app_manager import manager
from api.state import contexts
from auth.dependencies import get_current_user
from api.dependencies.deps import get_db
from infra.database.models.analysis import AnalysisModel
from uuid import uuid4
import json

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/{dataset_id}/summary")
def dataset_summary(dataset_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = int(user["sub"]) 

    key = (user_id, dataset_id)
    if key not in contexts:
        raise HTTPException(status_code=404, detail="Dataset não encontrado na memória.")
    
    ctx = contexts[key]
    summary = ctx.dataframe.describe().to_dict()
    
    # Salvar no BD
    analysis = AnalysisModel(
        id=str(uuid4()),
        user_id=user_id,
        dataset_id=dataset_id,
        analysis_type="summary",
        result=json.dumps(summary)
    )
    db.add(analysis)
    db.commit()
    
    return {"summary": summary}

@router.get("/{dataset_id}/analysis")
def basic_analysis(dataset_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = int(user["sub"])

    key = (user_id, dataset_id)
    if key not in contexts:
        raise HTTPException(status_code=404, detail="Dataset não encontrado na memória.")
    
    ctx = contexts[key]
    analysis_result = manager.basic_analysis_uc.execute(ctx)
    
    # Salvar no BD
    analysis = AnalysisModel(
        id=str(uuid4()),
        user_id=user_id,
        dataset_id=dataset_id,
        analysis_type="basic",
        result=json.dumps(analysis_result)
    )
    db.add(analysis)
    db.commit()
    
    return {"analysis": analysis_result}