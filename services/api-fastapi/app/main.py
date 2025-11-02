import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from .deps import engine
from .models import Base
from .routes import auth, users, workflows

app = FastAPI(
    title="CluesStack (FastAPI)",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)

# Ensure tables exist (simple bootstrap)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(workflows.router)

@app.get("/healthz")
def health():
    return {"status": "ok"}
