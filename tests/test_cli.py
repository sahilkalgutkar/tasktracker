import io
import contextlib
import os
import tempfile
import unittest
from unittest import mock

from tasktracker.cli import main


class CliTestCase(unittest.TestCase):
    def setUp(self):
        # The CLI builds its own TaskTracker, so point the store at a temp file
        # through the env var rather than reaching into the object.
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        os.environ["TASKTRACKER_STORE"] = os.path.join(self.tmpdir.name, "tasks.json")
        self.addCleanup(os.environ.pop, "TASKTRACKER_STORE", None)

    def run_cli(self, *argv):
        out = io.StringIO()
        with mock.patch("sys.argv", ["tasktracker", *argv]), contextlib.redirect_stdout(out):
            main()
        return out.getvalue()


class TestCliActions(CliTestCase):
    def test_add_then_list_shows_the_task(self):
        self.run_cli("add", "--title", "Write tests", "--description", "For the CLI")
        self.assertIn("Write tests", self.run_cli("list"))

    def test_add_reports_success(self):
        output = self.run_cli("add", "--title", "Ship it", "--description", "Today")
        self.assertIn("added successfully", output)

    def test_list_on_an_empty_store(self):
        self.assertIn("No tasks found", self.run_cli("list"))

    def test_delete_removes_the_task(self):
        self.run_cli("add", "--title", "Temporary", "--description", "Short-lived")
        self.assertIn("deleted successfully", self.run_cli("delete", "--title", "Temporary"))
        self.assertIn("No tasks found", self.run_cli("list"))

    def test_done_marks_the_task(self):
        self.run_cli("add", "--title", "Chore", "--description", "Do it")
        self.assertIn("marked as done", self.run_cli("done", "--title", "Chore"))
        self.assertIn("status=done", self.run_cli("list"))

    def test_inactive_marks_the_task(self):
        self.run_cli("add", "--title", "Parked", "--description", "Later")
        self.assertIn("marked as inactive", self.run_cli("inactive", "--title", "Parked"))
        self.assertIn("status=inactive", self.run_cli("list"))


class TestCliMissingArguments(CliTestCase):
    def test_add_without_a_description(self):
        self.assertIn("both title and description", self.run_cli("add", "--title", "Lonely"))

    def test_add_without_a_title(self):
        self.assertIn("both title and description", self.run_cli("add", "--description", "Lonely"))

    def test_delete_without_a_title(self):
        self.assertIn("provide the title", self.run_cli("delete"))

    def test_done_without_a_title(self):
        self.assertIn("provide the title", self.run_cli("done"))

    def test_inactive_without_a_title(self):
        self.assertIn("provide the title", self.run_cli("inactive"))

    def test_an_unknown_action_is_rejected(self):
        with mock.patch("sys.argv", ["tasktracker", "explode"]):
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    main()


if __name__ == "__main__":
    unittest.main()
