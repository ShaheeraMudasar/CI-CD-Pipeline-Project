from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .routers import api, web


def _register_routers(app: FastAPI) -> None:
    """Include all your API and web routers."""
    app.include_router(api.router, prefix="/api/v1")
    app.include_router(web.router)


def _mount_static_files(app: FastAPI) -> None:
    """Serve /static from the right folder."""
    # Use Path to build a stable, import-relative path
    static_dir = Path(__file__).parent / "static"
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


def _register_misc_routes(app: FastAPI) -> None:
    """Any one-off routes (robots.txt, healthchecks, etc.)."""
    # Rather than a decorator at import time, register via add_api_route
    robots_path = Path(__file__).parent / "static" / "robots.txt"
    app.add_api_route(
        "/robots.txt",
        endpoint=lambda: FileResponse(str(robots_path), media_type="text/plain"),
        methods=["GET"],
        include_in_schema=False,
    )


def create_app() -> FastAPI:
    """
    Build and return the FastAPI application.
    All mounting, router-registration, and route definitions happen here.
    """
    app = FastAPI(title="DevOps1-bloggen")
    _register_routers(app)
    _mount_static_files(app)
    _register_misc_routes(app)
    return app
