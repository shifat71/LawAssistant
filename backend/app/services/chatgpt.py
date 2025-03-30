import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from datetime import datetime
from app.models.models import Response
from fastapi import Depends
from ..database import get_db
from sqlalchemy.orm import Session

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

SYSTEM_MESSAGE = {"role": "system", "content": "You are a helpful chatbot. Give short precise answer not more then 2-3 lines."}
    

async def generate_chat_response(prompt: str, user_digit: str, db: Session = Depends(get_db)):
    try:
        # Get LLM response (existing implementation)
        completion = await client.chat.completions.create(
            model="qwen1.5-14b-chat",
            messages = [
                SYSTEM_MESSAGE,
                {"role": "user", "content": prompt}
            ]
        )
        response_text = completion.choices[0].message.content.strip()
        
        # Create database record
        db_response = Response(
            prompt=prompt,
            response=response_text,
            user_digit=user_digit,
            created_at=datetime.utcnow()
        )
        
        db.add(db_response)
        db.commit()
        db.refresh(db_response)
        
        return response_text, db_response.created_at
        
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Error: {str(e)}")