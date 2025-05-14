from fastapi import APIRouter, HTTPException #HTTPException dont uses yet
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health")
async def health():
  
  return JSONResponse(content={"status": "ok"}, status_code = 200)
