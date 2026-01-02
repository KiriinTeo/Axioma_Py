from fastapi import APIRouter
from application.app_manager import manager
from api.state import contexts
import io
import base64

router = APIRouter(prefix="/plot", tags=["Plot"])

@router.post("/generate")
def generate_plot(
    dataset_id: int,
    plot_type: str,
    x: str | None = None,
    y: str | None = None
):
    ctx = contexts[dataset_id]
    fig, ax = manager.generate_plot_uc.execute(
        ctx=ctx,
        plot_type=plot_type,
        x=x,
        y=y
    )

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    encoded = base64.b64encode(buf.read()).decode()
    return {"image": encoded}
