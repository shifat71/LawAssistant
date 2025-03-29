from pydantic import BaseModel, Field
from datetime import datetime

class ChatRequest(BaseModel):
    prompt: str
    user_digit: str = Field(
        ...,
        min_length=4,
        max_length=4,
        pattern=r"^\d{4}$"  # Changed from regex to pattern
    )

class ChatResponse(BaseModel):
    response: str
    user_digit: str
    timestamp: datetime