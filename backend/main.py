from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles

from api.base import api_router
from apps.base import app_router
from db.session import engine
from core.config import settings
from db.base_class import Base


def include_router(app):
    app.include_router(api_router)
    app.include_router(app_router)


def configure_static_files(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")
    

def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    configure_static_files(app)
    include_router(app)
    return app


app = start_application()


