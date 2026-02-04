from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from application.app_manager import manager
from api.state import contexts
from auth.dependencies import get_current_user
from api.dependencies.deps import get_db
from infra.database.models.plot import PlotModel
from uuid import uuid4
import io
import base64

router = APIRouter(prefix="/plot", tags=["Plot"])

@router.post("/generate")
def generate_plot(
    dataset_id: str = Body(...),
    plot_type: str = Body(...),
    x: str | None = Body(None),
    y: str | None = Body(None),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = int(user["sub"])
    key = (user_id, dataset_id)
    if key not in contexts:
        raise HTTPException(status_code=404, detail="Dataset não encontrado na memória.")
    
    ctx = contexts[key]

    try:
        fig, ax = manager.generate_plot_uc.execute(
            ctx=ctx,
            plot_type=plot_type,
            x=x,
            y=y,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    
    plot_model = PlotModel(
        id=str(uuid4()),
        user_id=user_id,
        dataset_id=dataset_id,
        plot_type=plot_type,
        x_axis=x,
        y_axis=y
    )
    db.add(plot_model)
    db.commit()

    encoded = base64.b64encode(buf.read()).decode()
    return {"image": encoded}
