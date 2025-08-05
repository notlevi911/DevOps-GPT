from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from datetime import datetime

from ..models.schemas import ChatMessageRequest, ChatMessageResponse, MessageSender
from ..services.langchain_service import langchain_service

router = APIRouter(prefix="/chat", tags=["chat"])

# In-memory storage (replace with DB later)
chat_history: List[ChatMessageResponse] = []

@router.post("", response_model=ChatMessageResponse)
async def send_message(message: ChatMessageRequest):
    try:
        # Add user message to history
        user_msg = ChatMessageResponse(
            id=str(uuid.uuid4()),
            text=message.message,
            sender=MessageSender.USER,
            timestamp=datetime.now()
        )
        chat_history.append(user_msg)
        
        # Get AI response
        bot_response = await langchain_service.chat(message.message)
        
        # Add bot message to history
        bot_msg = ChatMessageResponse(
            id=str(uuid.uuid4()),
            text=bot_response,
            sender=MessageSender.BOT,
            timestamp=datetime.now()
        )
        chat_history.append(bot_msg)
        
        return bot_msg
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@router.get("/history", response_model=List[ChatMessageResponse])
async def get_chat_history():
    return chat_history

@router.delete("/history")
async def clear_chat_history():
    global chat_history
    chat_history.clear()
    return {"message": "Chat history cleared"}