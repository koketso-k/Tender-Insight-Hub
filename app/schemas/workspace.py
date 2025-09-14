from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteOut(NoteBase):
    id: UUID
    created_by: UUID
    updated_at: datetime

    class Config:
        orm_mode = True


class ProjectLinkBase(BaseModel):
    link_type: str
    reference: str


class ProjectLinkCreate(ProjectLinkBase):
    pass


class ProjectLinkOut(ProjectLinkBase):
    id: UUID
    added_by: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class WorkspaceBase(BaseModel):
    name: str
    description: Optional[str]


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceOut(WorkspaceBase):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
