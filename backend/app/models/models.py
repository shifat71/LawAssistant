from sqlalchemy import Column, String, Integer, DateTime  # <-- Add DateTime here
from datetime import datetime
from app.database import Base

class Demo(Base):
    __tablename__ = "user"
    username = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String(10), nullable=False)

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String(500), nullable=False)
    response = Column(String(2000), nullable=False)
    user_digit = Column(String(4), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # Now DateTime is recognized