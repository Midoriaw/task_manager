import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import crud

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_tasks():
    crud.tasks.clear()
    yield
    crud.tasks.clear()


def test_create_task():
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Desc"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "created"
    assert "id" in data


def test_get_task():
    response = client.post("/tasks/", json={"title": "Task 1"})
    task_id = response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Task 1"


def test_get_tasks_list():
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2"})

    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {task["title"] for task in data} == {"Task 1", "Task 2"}


def test_update_task():
    response = client.post("/tasks/", json={"title": "Old Title"})
    task_id = response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "New Title", "status": "in_progress"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["status"] == "in_progress"


def test_delete_task():
    response = client.post("/tasks/", json={"title": "Delete me"})
    task_id = response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404


# --- ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ДЛЯ 100% ПОКРЫТИЯ ---

def test_update_nonexistent_task():
    fake_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.put(f"/tasks/{fake_id}", json={"title": "Ghost"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_nonexistent_task():
    fake_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.delete(f"/tasks/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_get_nonexistent_task():
    fake_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.get(f"/tasks/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_task_model_class():
    import uuid
    from app.models import Task, TaskStatus

    task_id = uuid.uuid4()
    task = Task(task_id, "Title", "Desc", TaskStatus.CREATED)

    assert task.id == task_id
    assert task.title == "Title"
    assert task.description == "Desc"
    assert task.status == TaskStatus.CREATED
