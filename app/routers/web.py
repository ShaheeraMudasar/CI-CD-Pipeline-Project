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
    print("[ROUTE] GET / - Listing posts")
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db = get_dynamo_client()
        posts = db.list_posts()
        print(f"[ROUTE] GET / - Found {len(posts)} posts")
        return templates.TemplateResponse(
            "index.html", {"request": request, "timestamp": now, "posts": posts}
        )
    except Exception as e:
        print(f"[ERROR] GET / failed: {e!s}")
        import traceback

        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise


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
    print(f"[ROUTE] GET /posts/{post_id}")
    try:
        db = get_dynamo_client()
        post = db.get_post(post_id)
        if not post:
            print(f"[ROUTE] GET /posts/{post_id} - Post not found")
            return HTMLResponse(status_code=404, content="Post not found")

        print(f"[ROUTE] GET /posts/{post_id} - Post found")
        return templates.TemplateResponse("post.html", {"request": request, "post": post})
    except Exception as e:
        print(f"[ERROR] GET /posts/{post_id} failed: {e!s}")
        import traceback

        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise


@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    print("[ROUTE] GET /admin - Admin panel requested")
    if not feature_admin_enabled():
        print("[ROUTE] GET /admin - Admin functionality disabled")
        raise HTTPException(status_code=403, detail="Adminfunktionalitet är avstängd")

    try:
        db = get_dynamo_client()
        posts = db.list_posts()
        print(f"[ROUTE] GET /admin - Loaded {len(posts)} posts")
        return templates.TemplateResponse(
            "admin.html", {"request": request, "error": None, "posts": posts}
        )
    except Exception as e:
        print(f"[ERROR] GET /admin failed: {e!s}")
        import traceback

        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise


@router.post("/admin/create", response_class=HTMLResponse)
async def create_post_from_form(
    request: Request,
    password: str = Form(...),
    title: str = Form(...),
    image_url: str = Form(...),
    image_text: str = Form(...),
):
    print("[ROUTE] POST /admin/create - Creating new post")
    if not feature_admin_enabled():
        print("[ROUTE] POST /admin/create - Admin functionality disabled")
        raise HTTPException(status_code=403, detail="Adminfunktionalitet är avstängd")

    if password != get_admin_password():
        print("[ROUTE] POST /admin/create - Invalid password")
        return templates.TemplateResponse(
            "admin.html", {"request": request, "error": "Fel lösenord"}
        )

    try:
        post_data = PostIn(title=title, image_url=image_url, image_text=image_text)
        db = get_dynamo_client()
        post_id = db.create_post(post_data)
        print(f"[ROUTE] POST /admin/create - Successfully created post {post_id}")
        return RedirectResponse("/", status_code=302)
    except Exception as e:
        print(f"[ERROR] POST /admin/create failed: {e!s}")
        import traceback

        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise


@router.post("/admin/delete", response_class=HTMLResponse)
async def delete_post_from_form(
    request: Request, password: str = Form(...), post_id: str = Form(...)
):
    print(f"[ROUTE] POST /admin/delete - Deleting post {post_id}")
    if not feature_admin_enabled():
        print("[ROUTE] POST /admin/delete - Admin functionality disabled")
        raise HTTPException(status_code=403, detail="Adminfunktionalitet är avstängd")

    if password != get_admin_password():
        print("[ROUTE] POST /admin/delete - Invalid password")
        return templates.TemplateResponse(
            "admin.html", {"request": request, "error": "Fel lösenord"}
        )

    try:
        db = get_dynamo_client()
        success = db.delete_post(post_id)
        if success:
            print(f"[ROUTE] POST /admin/delete - Successfully deleted post {post_id}")
        else:
            print(f"[ROUTE] POST /admin/delete - Post {post_id} not found")
        return RedirectResponse("/", status_code=302)
    except Exception as e:
        print(f"[ERROR] POST /admin/delete failed: {e!s}")
        import traceback

        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        raise


@router.get("/status", response_class=HTMLResponse)
async def status(request: Request):
    health_data = {
        "status": "Healthy",
        "commit_hash": get_git_commit_hash(),
        "uptime": get_uptime(),
    }
    print("[ROUTE] GET /status - Status check requested")
    return templates.TemplateResponse("status.html", {"request": request, **health_data})
