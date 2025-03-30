from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    name: str
    age: int
    sex: str

class UserResponse(UserCreate):
    username: str
    model_config = ConfigDict(from_attributes=True)  # Replacement for orm_mode