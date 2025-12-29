from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from app.core.config import DATA_DIR
from app.core.logging import configure_logging
from app.api.routes import health, assets, jobs, extract, tryon
from app.services.storage import ensure_dirs


def create_app() -> FastAPI:
    configure_logging()
    ensure_dirs()
    app = FastAPI(title="NailArt API", version="0.1.0")
    app.mount("/static", StaticFiles(directory=DATA_DIR), name="static")

    api_router = APIRouter()
    api_router.include_router(health.router)
    api_router.include_router(assets.router)
    api_router.include_router(jobs.router)
    api_router.include_router(extract.router)
    api_router.include_router(tryon.router)

    app.include_router(api_router, prefix="/v1")
    return app


app = create_app()
