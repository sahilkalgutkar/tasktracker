import datetime
import json
import os

class Task:
    def __init__(self, title, description, status='active', created_at=None, updated_at=None):
        self.title = title
        self.description = description
        self.status = status  # Possible values: active, done, inactive
        self.created_at = created_at if created_at else datetime.datetime.now()
        self.updated_at = updated_at if updated_at else self.created_at

    def update(self, title=None, description=None, status=None):
        if title:
            self.title = title
        if description:
            self.description = description
        if status:
            self.status = status
        self.updated_at = datetime.datetime.now()

    def mark_done(self):
        self.status = 'done'
        self.updated_at = datetime.datetime.now()

    def mark_inactive(self):
        self.status = 'inactive'
        self.updated_at = datetime.datetime.now()

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data['title'],
            description=data['description'],
            status=data['status'],
            created_at=datetime.datetime.fromisoformat(data['created_at']),
            updated_at=datetime.datetime.fromisoformat(data['updated_at'])
        )

    def __str__(self):
        return (f"Task(title={self.title}, description={self.description}, status={self.status}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})")


class TaskTracker:
    STORAGE_FILE = 'tasks.json'

    def __init__(self):
        self.tasks = self.load_tasks()

    def add_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, title):
        self.tasks = [task for task in self.tasks if task.title != title]
        self.save_tasks()

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def update_task(self, title, new_title=None, new_description=None, new_status=None):
        task = self.get_task(title)
        if task:
            task.update(new_title, new_description, new_status)
            self.save_tasks()

    def mark_task_done(self, title):
        task = self.get_task(title)
        if task:
            task.mark_done()
            self.save_tasks()

    def mark_task_inactive(self, title):
        task = self.get_task(title)
        if task:
            task.mark_inactive()
            self.save_tasks()

    def list_tasks(self):
        return self.tasks

    def save_tasks(self):
        with open(self.STORAGE_FILE, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    def load_tasks(self):
        if os.path.exists(self.STORAGE_FILE):
            with open(self.STORAGE_FILE, 'r') as file:
                tasks_data = json.load(file)
                return [Task.from_dict(task_data) for task_data in tasks_data]
        return []
