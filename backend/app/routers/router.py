from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.models import Demo
from ..schemas.schema import UserCreate, UserResponse
from ..database import get_db

router = APIRouter(prefix="/api")

def generate_username(db: Session, name: str) -> str:
    # Extract last name
    last_name = name.strip().split()[-1].lower()
    
    # Find existing usernames with same base
    existing = db.query(Demo.username).filter(
        Demo.username.ilike(f"{last_name}_%")
    ).all()
    
    # Find highest sequence number
    max_num = 0
    for username in existing:
        try:
            num = int(username[0].split('_')[-1])
            max_num = max(max_num, num)
        except (IndexError, ValueError):
            continue
    
    # Format new username
    return f"{last_name}_{max_num + 1:04d}"

@router.post("/create-user", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Generate unique username
        username = generate_username(db, user.name)
        
        # Create user object
        db_user = Demo(
            username=username,
            name=user.name,
            age=user.age,
            sex=user.sex
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, 
            detail=f"Error creating user: {str(e)}"
        )