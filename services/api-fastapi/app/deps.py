import os, uuid
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi import Header
from jose import jwt, JWTError
from passlib.hash import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

JWT_SECRET = os.getenv("JWT_SECRET", "change")
JWT_ISS = os.getenv("JWT_ISS", "cluesstack")
JWT_AUD = os.getenv("JWT_AUD", "cluesstack-app")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(pw: str) -> str:
    return bcrypt.hash(pw)

def verify_password(pw: str, hashed: str) -> bool:
    return bcrypt.verify(pw, hashed)

def create_access_token(sub: str, name: str, email: str, expires_minutes: int = 15) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "name": name,
        "email": email,
        "iss": JWT_ISS,
        "aud": JWT_AUD,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def current_user(authorization: Optional[str] = Header(default=None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], audience=JWT_AUD, issuer=JWT_ISS)
        return {"id": payload["sub"], "name": payload["name"], "email": payload["email"]}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def gen_id(prefix: str) -> str:
    import uuid as _uuid
    return f"{prefix}_{_uuid.uuid4().hex[:10]}"
