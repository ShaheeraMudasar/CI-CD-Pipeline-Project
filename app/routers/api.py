from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/health")
async def health():
  # TODO: implementera
  raise NotImplementedError
