from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..deps import current_user, get_db, gen_id
from ..models import Workflow

router = APIRouter(prefix="/workflows", tags=["workflows"])

class WorkflowIn(BaseModel):
    project_id: str
    name: str
    tags: list[str] = []

@router.post("")
def create_workflow(payload: WorkflowIn, user=Depends(current_user), db: Session = Depends(get_db)):
    wf = Workflow(id=gen_id("wfl"), project_id=payload.project_id, name=payload.name,
                  tags=",".join(payload.tags), created_by=user["id"])
    db.add(wf); db.commit()
    return {"id": wf.id, "name": wf.name, "project_id": wf.project_id, "tags": payload.tags}

@router.get("")
def list_workflows(db: Session = Depends(get_db)):
    rows = db.query(Workflow).order_by(Workflow.updated_at.desc()).limit(50).all()
    return [{"id": w.id, "name": w.name, "project_id": w.project_id, "tags": (w.tags or "").split(",")} for w in rows]
