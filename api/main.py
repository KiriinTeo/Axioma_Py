from fastapi import FastAPI
from application.app_manager import ApplicationManager

app = FastAPI(title="Axioma Py")

manager = ApplicationManager()

from api.routes import dataset, plot, analysis, filtro, exportar, auth, saude

app.include_router(dataset.router)
app.include_router(plot.router)
app.include_router(analysis.router)
app.include_router(filtro.router)
app.include_router(exportar.router)
app.include_router(auth.router)
app.include_router(saude.router)