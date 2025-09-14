from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])


@router.post("/", response_model=schemas.WorkspaceOut)
def create_workspace(workspace: schemas.WorkspaceCreate, db: Session = Depends(get_db)):
    new_ws = models.Workspace(name=workspace.name, description=workspace.description)
    db.add(new_ws)
    db.commit()
    db.refresh(new_ws)
    return new_ws


@router.get("/", response_model=list[schemas.WorkspaceOut])
def list_workspaces(db: Session = Depends(get_db)):
    return db.query(models.Workspace).all()


@router.post("/{workspace_id}/notes", response_model=schemas.NoteOut)
def create_note(workspace_id: UUID, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    ws = db.query(models.Workspace).filter_by(id=workspace_id).first()
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    new_note = models.Note(workspace_id=workspace_id, title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@router.post("/{workspace_id}/links", response_model=schemas.ProjectLinkOut)
def create_link(workspace_id: UUID, link: schemas.ProjectLinkCreate, db: Session = Depends(get_db)):
    ws = db.query(models.Workspace).filter_by(id=workspace_id).first()
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    new_link = models.ProjectLink(workspace_id=workspace_id, link_type=link.link_type, reference=link.reference)
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link
