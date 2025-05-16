from fastapi import APIRouter  # HTTPException dont uses yet
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health")
async def health():
    return JSONResponse(content={"status": "ok"}, status_code=200) #send status by string and code as JSON-format
