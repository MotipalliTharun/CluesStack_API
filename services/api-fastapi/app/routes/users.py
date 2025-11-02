from fastapi import APIRouter, Depends
from ..deps import current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def me(user=Depends(current_user)):
    return {"id": user["id"], "name": user["name"], "email": user["email"]}
