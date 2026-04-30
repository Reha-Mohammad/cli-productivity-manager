import os
import tempfile
import unittest

from manager import TaskManager
from storage import Storage


class TestStorage(unittest.TestCase):
    def test_save_and_load_tasks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "tasks.json")
            storage = Storage(file_path)

            manager = TaskManager()
            manager.add_task(
                "Study Django",
                "Read models",
                "2026-05-01",
                "high",
                "study, django"
            )

            storage.save_tasks(manager.tasks)
            loaded_tasks = storage.load_tasks()

            self.assertEqual(len(loaded_tasks), 1)
            self.assertEqual(loaded_tasks[0].title, "Study Django")
            self.assertEqual(loaded_tasks[0].priority, "high")
            self.assertEqual(loaded_tasks[0].tags, ["study", "django"])

    def test_load_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "missing.json")
            storage = Storage(file_path)

            loaded_tasks = storage.load_tasks()

            self.assertEqual(loaded_tasks, [])


if __name__ == "__main__":
    unittest.main()


    # python -m unittest discover -s tests