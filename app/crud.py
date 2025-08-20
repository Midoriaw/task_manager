import uuid
from typing import Dict
from .schemas import TaskCreate, TaskUpdate, TaskOut
from .models import TaskStatus

# In-memory storage
tasks: Dict[uuid.UUID, TaskOut] = {}


def create_task(task_in: TaskCreate) -> TaskOut:
    task_id = uuid.uuid4()
    task = TaskOut(id=task_id, status=TaskStatus.CREATED, **task_in.model_dump())
    tasks[task_id] = task
    return task


def get_task(task_id: uuid.UUID) -> TaskOut | None:
    return tasks.get(task_id)


def get_tasks() -> list[TaskOut]:
    return list(tasks.values())


def update_task(task_id: uuid.UUID, task_in: TaskUpdate) -> TaskOut | None:
    task = tasks.get(task_id)
    if not task:
        return None

    updated_data = task.model_dump()
    for field, value in task_in.model_dump(exclude_unset=True).items():
        updated_data[field] = value

    updated_task = TaskOut(**updated_data)
    tasks[task_id] = updated_task
    return updated_task


def delete_task(task_id: uuid.UUID) -> bool:
    if task_id not in tasks:
        return False
    del tasks[task_id]
    return True
