# app/main.py
from fastapi import FastAPI
from app.models.db import init_db
from app.api import health, whatsapp

def create_app() -> FastAPI:
    app = FastAPI(title="Hygen Real Estate MVP1")

    app.include_router(health.router, tags=["health"])
    app.include_router(whatsapp.router, prefix="/webhook", tags=["whatsapp"])

    @app.on_event("startup")
    async def on_startup():
        init_db()

    return app


app = create_app()
