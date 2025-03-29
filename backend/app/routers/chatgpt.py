from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.chatgpt import ChatRequest, ChatResponse
from app.services.chatgpt import generate_chat_response
from app.database import get_db

router = APIRouter(prefix="/api/chat")

@router.post("/prompt", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest, 
    db: Session = Depends(get_db)
):
    try:
        response, timestamp = await generate_chat_response(
            request.prompt,
            request.user_digit,
            db
        )
        return {
            "response": response,
            "user_digit": request.user_digit,
            "timestamp": timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))