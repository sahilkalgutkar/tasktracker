import datetime

class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.created_at = datetime.datetime.now()
        self.updated_at = self.created_at
        self.status = 'active'  # possible values: active, done, inactive

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

    def __str__(self):
        return (f"Task(title={self.title}, description={self.description}, status={self.status}, "
                f"created_at={self.created_at}, updated_at={self.updated_at})")


class TaskTracker:
    def __init__(self):
        self.tasks = []  # In-memory storage for tasks

    def add_task(self, title, description):
        task = Task(title, description)
        self.tasks.append(task)

    def delete_task(self, title):
        self.tasks = [task for task in self.tasks if task.title != title]

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def update_task(self, title, new_title=None, new_description=None, new_status=None):
        task = self.get_task(title)
        if task:
            task.update(new_title, new_description, new_status)

    def mark_task_done(self, title):
        task = self.get_task(title)
        if task:
            task.mark_done()

    def mark_task_inactive(self, title):
        task = self.get_task(title)
        if task:
            task.mark_inactive()

    def list_tasks(self):
        return self.tasks

if __name__ == "__main__":
    tracker = TaskTracker()
    tracker.add_task("Sample Task 1", "This is the first sample task.")
    tracker.add_task("Sample Task 2", "This is the second sample task.")
    tracker.mark_task_done("Sample Task 1")
    tracker.mark_task_inactive("Sample Task 2")

    for task in tracker.list_tasks():
        print(task)
