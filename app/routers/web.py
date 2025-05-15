# app/routers/web.py
import subprocess
import time
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

start_time = time.time()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return templates.TemplateResponse("index.html", {"request": request, "timestamp": now})


def get_git_commit_hash() -> str:
    try:
        # Get the latest commit hash
        commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
        return commit_hash
    except subprocess.CalledProcessError:
        return "Unknown git command"


def get_uptime() -> str:
    # Calc uptime in s, m, h
    uptime_seconds = int(time.time() - start_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{hours}h {minutes}m {seconds}s"


def get_uptime() -> str:
    # Calc uptime in s, m, h
    uptime_seconds = int(time.time() - start_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{hours}h {minutes}m {seconds}s"


@router.get("/status", response_class=HTMLResponse)
async def status(request: Request):
    # commit_hash = get_git_commit_hash()
    health_data = {
        "status": "Healthy",
        "commit_hash": get_git_commit_hash(),
        "uptime": get_uptime(),
    }
    return templates.TemplateResponse("status.html", {"request": request, **health_data})
