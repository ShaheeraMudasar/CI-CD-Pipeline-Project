from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.storage.ddb import get_dynamo_client

router = APIRouter()


@router.get("/health")
async def health():
    # Sends status as JSON
    return JSONResponse(content={"status": "ok"}, status_code=200)


@router.get("/posts")
async def list_posts():
    """Returnera lista med alla inlägg via JSON API."""
    db = get_dynamo_client()
    posts = db.list_posts()
    return [{"id": post.id, "title": post.title} for post in posts]
