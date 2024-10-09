import unittest
from tasktracker.taskl import Task, TaskTracker

class TestTaskTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = TaskTracker()

    def test_add_task(self):
        self.tracker.add_task("Test Task", "Test Description")
        self.assertEqual(len(self.tracker.tasks), 1)

    def test_delete_task(self):
        self.tracker.add_task("Test Task", "Test Description")
        self.tracker.delete_task("Test Task")
        self.assertEqual(len(self.tracker.tasks), 0)

    def test_mark_task_done(self):
        self.tracker.add_task("Test Task", "Test Description")
        self.tracker.mark_task_done("Test Task")
        task = self.tracker.get_task("Test Task")
        self.assertEqual(task.status, "done")

    def test_mark_task_inactive(self):
        self.tracker.add_task("Test Task", "Test Description")
        self.tracker.mark_task_inactive("Test Task")
        task = self.tracker.get_task("Test Task")
        self.assertEqual(task.status, "inactive")

if __name__ == "__main__":
    unittest.main()
