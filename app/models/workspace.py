from sqlalchemy import Column, String, Text, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime

from app.database import Base


class WorkspaceRole(enum.Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    members = relationship("WorkspaceMember", back_populates="workspace")
    notes = relationship("Note", back_populates="workspace")
    links = relationship("ProjectLink", back_populates="workspace")


class WorkspaceMember(Base):
    __tablename__ = "workspace_members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    role = Column(Enum(WorkspaceRole), default=WorkspaceRole.viewer)

    workspace = relationship("Workspace", back_populates="members")


class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    title = Column(String(200))
    content = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    workspace = relationship("Workspace", back_populates="notes")


class ProjectLink(Base):
    __tablename__ = "project_links"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"))
    link_type = Column(String(20))  # tender, url, document
    reference = Column(Text)
    added_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("Workspace", back_populates="links")
