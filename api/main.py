from fastapi import FastAPI
from application.app_manager import ApplicationManager
from contextlib import asynccontextmanager
from infra.logging.logger import setup_logger
from infra.database.base import Base
from infra.database.connection import engine

logger = setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando o Axioma...")

    app.state.manager = ApplicationManager()
    Base.metadata.create_all(bind=engine)
    yield

    logger.info("Finalizando o Axioma...")

app = FastAPI(title="Axioma Py",lifespan=lifespan)

from api.routes import dataset, plot, analysis, filtro, exportar, auth, saude

app.include_router(dataset.router)
app.include_router(plot.router)
app.include_router(analysis.router)
app.include_router(filtro.router)
app.include_router(exportar.router)
app.include_router(auth.router)
app.include_router(saude.router)