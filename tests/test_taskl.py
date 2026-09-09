import datetime
import os
import tempfile
import unittest

from tasktracker.taskl import Task, TaskTracker


class TestTaskTracker(unittest.TestCase):
    def setUp(self):
        # Each test gets its own store, so a run never inherits state from the
        # last one and never writes into the working directory.
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.store = os.path.join(self.tmpdir.name, "tasks.json")
        self.tracker = TaskTracker(storage_file=self.store)

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
        self.assertEqual(self.tracker.get_task("Test Task").status, "done")

    def test_mark_task_inactive(self):
        self.tracker.add_task("Test Task", "Test Description")
        self.tracker.mark_task_inactive("Test Task")
        self.assertEqual(self.tracker.get_task("Test Task").status, "inactive")

    def test_repeated_runs_do_not_accumulate(self):
        # The old suite shared one tasks.json, so a second run started with the
        # previous run's tasks already loaded and this count came out wrong.
        for _ in range(3):
            tracker = TaskTracker(storage_file=self.store)
            tracker.add_task("Only", "One at a time")
            tracker.delete_task("Only")
        self.assertEqual(TaskTracker(storage_file=self.store).tasks, [])

    def test_tasks_survive_a_reload(self):
        self.tracker.add_task("Persisted", "Written to disk")
        reloaded = TaskTracker(storage_file=self.store)
        self.assertEqual(len(reloaded.tasks), 1)
        self.assertEqual(reloaded.tasks[0].description, "Written to disk")

    def test_env_var_selects_the_store(self):
        other = os.path.join(self.tmpdir.name, "from-env.json")
        os.environ["TASKTRACKER_STORE"] = other
        self.addCleanup(os.environ.pop, "TASKTRACKER_STORE", None)
        TaskTracker().add_task("Env", "Chosen by TASKTRACKER_STORE")
        self.assertTrue(os.path.exists(other))

    def test_get_task_returns_none_when_absent(self):
        self.assertIsNone(self.tracker.get_task("Never added"))

    def test_update_task_changes_fields(self):
        self.tracker.add_task("Old", "Old description")
        self.tracker.update_task("Old", new_title="New", new_status="done")
        self.assertIsNone(self.tracker.get_task("Old"))
        self.assertEqual(self.tracker.get_task("New").status, "done")

    def test_update_task_on_missing_title_is_a_no_op(self):
        self.tracker.update_task("Missing", new_title="Irrelevant")
        self.assertEqual(self.tracker.tasks, [])

    def test_list_tasks_returns_everything_added(self):
        self.tracker.add_task("First", "1")
        self.tracker.add_task("Second", "2")
        self.assertEqual([t.title for t in self.tracker.list_tasks()], ["First", "Second"])


class TestTask(unittest.TestCase):
    def test_round_trips_through_a_dict(self):
        task = Task("Title", "Description")
        restored = Task.from_dict(task.to_dict())
        self.assertEqual(restored.title, task.title)
        self.assertEqual(restored.status, task.status)
        self.assertEqual(restored.created_at, task.created_at)

    def test_new_task_starts_active(self):
        self.assertEqual(Task("T", "D").status, "active")

    def test_update_bumps_updated_at(self):
        task = Task("T", "D", created_at=datetime.datetime(2024, 1, 1))
        task.update(description="Changed")
        self.assertGreater(task.updated_at, task.created_at)

    def test_str_mentions_the_title_and_status(self):
        text = str(Task("Buy milk", "From the corner shop"))
        self.assertIn("Buy milk", text)
        self.assertIn("active", text)


if __name__ == "__main__":
    unittest.main()
