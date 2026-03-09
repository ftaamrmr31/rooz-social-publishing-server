from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

# Create an APIRouter instance for user endpoints
users_router = APIRouter()

# Endpoint to create a new user
@users_router.post("", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Create a new User object with the provided data
    db_user = User(
        email=user.email,
        full_name=user.full_name
    )
    # Add the user to the database session
    db.add(db_user)
    # Commit the transaction to save the user
    db.commit()
    # Refresh the user to get the generated id and created_at
    db.refresh(db_user)
    # Return the created user
    return db_user

# Endpoint to get a list of all users
@users_router.get("", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db)):
    # Query all users from the database
    return db.query(User).all()