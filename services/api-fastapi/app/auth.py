from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from .deps import get_db, hash_password, verify_password, create_access_token, gen_id
from .models import User

class RegisterIn(BaseModel):
    email: EmailStr
    name: str
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=422, detail="email already in use")
    u = User(id=gen_id("usr"), email=payload.email, name=payload.name, password_hash=hash_password(payload.password))
    db.add(u); db.commit()
    token = create_access_token(u.id, u.name, u.email)
    return {"access_token": token, "user": {"id": u.id, "name": u.name, "email": u.email}}

@router.post("/login")
def login(payload: LoginIn, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.email == payload.email).first()
    if not u or not verify_password(payload.password, u.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = create_access_token(u.id, u.name, u.email)
    return {"access_token": token, "user": {"id": u.id, "name": u.name, "email": u.email}}
