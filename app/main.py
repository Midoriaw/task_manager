from fastapi import FastAPI, HTTPException
import uuid
from . import crud
from .schemas import TaskCreate, TaskUpdate, TaskOut

app = FastAPI(title="Task Manager API")


@app.post("/tasks/", response_model=TaskOut)
def create_task(task_in: TaskCreate):
    return crud.create_task(task_in)


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: uuid.UUID):
    task = crud.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/tasks/", response_model=list[TaskOut])
def get_tasks():
    return crud.get_tasks()


@app.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: uuid.UUID, task_in: TaskUpdate):
    task = crud.update_task(task_id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: uuid.UUID):
    deleted = crud.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"ok": True}
