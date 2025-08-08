from fastapi import APIRouter  # HTTPException dont uses yet
from fastapi.responses import JSONResponse

from app.storage.ddb import get_dynamo_client

router = APIRouter()


@router.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"}, status_code=200)  # Sends status as JSON

@router.get("/posts")
async def list_posts():
    """Returnera lista med alla inlägg via JSON API."""
    db = get_dynamo_client()
    posts = db.list_posts()
    return [{"id": post.id, "title": post.title} for post in posts]
