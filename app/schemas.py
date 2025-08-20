import uuid
from typing import Optional
from pydantic import BaseModel, Field
from .models import TaskStatus


class TaskBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class TaskOut(TaskBase):
    id: uuid.UUID
    status: TaskStatus
