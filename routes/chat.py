from fastapi import APIRouter

router = APIRouter()

@router.get("/chat/status")
async def chat_status():
    return {"status": "Chat engine offline - Phase 1 stubs"}