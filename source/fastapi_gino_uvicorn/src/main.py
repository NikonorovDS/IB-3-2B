from fastapi import FastAPI
from custom_logging import CustomizeLogger
from core.config import settings
from fastapi.staticfiles import StaticFiles
from gino.ext.starlette import Gino
from pathlib import Path
import logging
import os
logger = logging.getLogger(__name__)

config_path=Path(__file__).with_name("logging_config.json")


app : FastAPI = FastAPI(title=settings.PROJECT_NAME,version=settings.VERSION)
logger = CustomizeLogger.make_logger(config_path)
app.logger = logger
app.mount("/static", StaticFiles(directory="static"), name="static")
db : Gino = Gino(dsn=settings.get_postgres_dsn())

db.init_app(app)

from api.api_v1.api import usersRouter, pagesRouter

app.include_router(usersRouter, prefix=settings.API_VERSION_STR, tags=['Users'])

app.include_router(pagesRouter, prefix=settings.API_VERSION_STR, tags=['Pages'])
