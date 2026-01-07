from fastapi import APIRouter, Depends
from application.app_manager import manager
from api.state import contexts
from auth.dependencies import get_current_user
from sqlalchemy.orm import Session
from api.dependencies.db import get_db
import io
import base64

router = APIRouter(prefix="/plot", tags=["Plot"])

@router.post("/generate")
def generate_plot(
    dataset_id: str,
    plot_type: str,
    x: str | None = None,
    y: str | None = None,
    user: dict = Depends(get_current_user)
):
    user_id = int(user["sub"])
    ctx = contexts[(user_id, dataset_id)]
    fig, ax = manager.generate_plot_uc.execute(
        ctx=ctx,
        plot_type=plot_type,
        x=x,
        y=y,
    )

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    encoded = base64.b64encode(buf.read()).decode()
    return {"image": encoded}
