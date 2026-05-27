from fastapi import APIRouter

router = APIRouter()

@router.get("/quotes/status")
async def quotes_status():
    return {"status": "Quotes engine offline - Phase 1 stubs"}