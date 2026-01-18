from fastapi import APIRouter, Depends, Body, HTTPException
from application.app_manager import manager
from api.state import contexts
from auth.dependencies import get_current_user
import io
import base64

router = APIRouter(prefix="/plot", tags=["Plot"])

@router.post("/generate")
def generate_plot(
    dataset_id: str = Body(...),
    plot_type: str = Body(...),
    x: str | None = Body(None),
    y: str | None = Body(None),
    user: dict = Depends(get_current_user)
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

    encoded = base64.b64encode(buf.read()).decode()
    return {"image": encoded}
