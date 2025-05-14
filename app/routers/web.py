# app/routers/web.py
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import subprocess
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return templates.TemplateResponse("index.html", {"request": request, "timestamp": now})


def get_git_commit_hash() -> str:
    try:
        # Get the latest commit hash
        commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
        return commit_hash
    except subprocess.CalledProcessError:
        return "Unknown git command"

@router.get("/status", response_class=HTMLResponse)
async def status(request: Request):
    commit_hash = get_git_commit_hash()
    return templates.TemplateResponse(
        "status.html",
        { "request": request, "commit_hash": commit_hash }
    )
