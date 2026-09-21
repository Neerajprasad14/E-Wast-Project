import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.config import get_settings
from app.db import init_database

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        init_database()
        logger.info("PostgreSQL tables are ready.")
    except Exception:
        logger.warning("PostgreSQL is unavailable. E-waste features remain available; authentication will return setup guidance.")
    yield


app = FastAPI(title=settings.app_name, version="0.2.0", description="AI-assisted e-waste decision support. Demo recycler records are not official listings.", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)
