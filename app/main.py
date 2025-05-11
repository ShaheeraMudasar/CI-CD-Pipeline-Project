from fastapi import FastAPI
from .routers import api, web

def create_app() -> FastAPI:
    app = FastAPI(title="DevOps1-bloggen")
    app.include_router(api.router, prefix="/api/v1")
    app.include_router(web.router)
    return app

app = create_app()
