import structlog

from fastapi import FastAPI
from api import api_router

app = FastAPI(title="Tabungan API middle", version="2.0.0")
log = structlog.get_logger('uvicorn')

app.include_router(api_router)