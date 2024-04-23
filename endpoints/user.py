import csv
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from model import Role, User
from model.db import get_db
import bcrypt

router = APIRouter(prefix="/user", tags=["user"])


class UserCreate(BaseModel):
    username: str
    password: str
    role_name: str


@router.post("/create-user/")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if the role exists
    role = db.query(Role).filter(Role.role_name == user_data.role_name).first()
    if not role:
        raise HTTPException(status_code=400, detail=f"Role {user_data.role_name} does not exist")

    # Check if the username already exists
    user = db.query(User).filter(User.username == user_data.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())

    # Create new user
    new_user = User(
        username=user_data.username,
        password=hashed_password.decode('utf-8'),  # Save the hashed password as a string
        role_id=role.role_id
    )
    db.add(new_user)
    db.commit()
    return {"status": "success", "message": "User created successfully"}
