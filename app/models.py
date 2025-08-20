import enum
import uuid


class TaskStatus(str, enum.Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task:
    def __init__(self, id_: uuid.UUID, title: str, description: str | None, status: TaskStatus):
        self.id = id_
        self.title = title
        self.description = description
        self.status = status
