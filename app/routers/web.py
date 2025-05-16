# app/routers/web.py
import subprocess
import time
from datetime import datetime

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.env import feature_admin_enabled, get_admin_password
from app.models import PostIn
from app.storage.ddb import get_dynamo_client

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

start_time = time.time()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db = get_dynamo_client()
    posts = await db.list_posts()
    return templates.TemplateResponse(
        "index.html", {"request": request, "timestamp": now, "posts": posts}
    )


def get_git_commit_hash() -> str:
    try:
        # Get the latest commit hash
        # commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
        # return commit_hash
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return "Unknown git command"


def get_uptime() -> str:
    # Calc uptime in s, m, h
    uptime_seconds = int(time.time() - start_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{hours}h {minutes}m {seconds}s"

   


@router.get("/posts/{post_id}", response_class=HTMLResponse)
async def view_post(request: Request, post_id: str):
    db = get_dynamo_client()
    post = await db.get_post(post_id)
    if not post:
        return HTMLResponse(status_code=404, content="Post not found")

    return templates.TemplateResponse("post.html", {"request": request, "post": post})


@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    if not feature_admin_enabled():
        raise HTTPException(status_code=403, detail="Adminfunktionalitet är avstängd")

    db = get_dynamo_client()
    posts = await db.list_posts()
    return templates.TemplateResponse(
        "admin.html", {"request": request, "error": None, "posts": posts}
    )


@router.post("/admin/create", response_class=HTMLResponse)
async def create_post_from_form(
    request: Request,
    password: str = Form(...),
    title: str = Form(...),
    image_url: str = Form(...),
    image_text: str = Form(...),
):
    if not feature_admin_enabled():
        raise HTTPException(status_code=403, detail="Adminfunktionalitet är avstängd")

    if password != get_admin_password():
        return templates.TemplateResponse(
            "admin.html", {"request": request, "error": "Fel lösenord"}
        )

    post_data = PostIn(title=title, image_url=image_url, image_text=image_text)
    db = get_dynamo_client()
    await db.create_post(post_data)
    return RedirectResponse("/", status_code=302)


@router.post("/admin/delete", response_class=HTMLResponse)
async def delete_post_from_form(
    request: Request, password: str = Form(...), post_id: str = Form(...)
):
    if not feature_admin_enabled():
        raise HTTPException(status_code=403, detail="Adminfunktionalitet är avstängd")

    if password != get_admin_password():
        return templates.TemplateResponse(
            "admin.html", {"request": request, "error": "Fel lösenord"}
        )

    db = get_dynamo_client()
    await db.delete_post(post_id)
    return RedirectResponse("/", status_code=302)


@router.get("/status", response_class=HTMLResponse)
async def status(request: Request):
    health_data = {
        "status": "Healthy",
        "commit_hash": get_git_commit_hash(),
        "uptime": get_uptime(),
    }
    return templates.TemplateResponse("status.html", {"request": request, **health_data})
