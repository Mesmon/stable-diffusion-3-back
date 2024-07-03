from fastapi import APIRouter, HTTPException
from models import PromptRequest
from queue_manager import add_to_queue

router = APIRouter()

@router.post("/generate-image/")
async def generate_image(request: PromptRequest):
    try:
        add_to_queue(request)
        return {"status": "Request added to the queue"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
