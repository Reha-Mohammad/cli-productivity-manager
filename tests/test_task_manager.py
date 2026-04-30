import unittest
from manager import TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()

    def test_add_task_valid_data(self):
        task = self.manager.add_task(
            "Study Django",
            "Read about models",
            "2026-05-01",
            "high",
            "study, django"
        )
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Study Django")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.tags, ["study", "django"])
        self.assertEqual(len(self.manager.tasks), 1)

    def test_add_task_rejects_empty_title(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("", "Some description")

    def test_add_task_rejects_invalid_date(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("Task", due_date="2026/05/01")

    def test_add_task_rejects_invalid_priority(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("Task", priority="urgent")

    def test_complete_task(self):
        task = self.manager.add_task("Finish README")
        self.assertFalse(task.completed)

        result = self.manager.complete_task(task.id)

        self.assertTrue(result)
        self.assertTrue(task.completed)
        self.assertIsNotNone(task.completed_at)

    def test_delete_task(self):
        task = self.manager.add_task("Delete me")
        result = self.manager.delete_task(task.id)

        self.assertTrue(result)
        self.assertEqual(len(self.manager.tasks), 0)

    def test_search_by_title(self):
        self.manager.add_task("Learn Django")
        self.manager.add_task("Buy groceries")

        results = self.manager.search_tasks_by_title("django")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Learn Django")

    def test_filter_by_due_date(self):
        self.manager.add_task("Task A", due_date="2026-05-01")
        self.manager.add_task("Task B", due_date="2026-05-02")

        results = self.manager.filter_tasks_by_due_date("2026-05-01")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Task A")

    def test_filter_by_priority(self):
        self.manager.add_task("Task A", priority="low")
        self.manager.add_task("Task B", priority="high")

        results = self.manager.filter_tasks_by_priority("high")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Task B")

    def test_filter_by_tag(self):
        self.manager.add_task("Task A", tags=["study", "python"])
        self.manager.add_task("Task B", tags=["work"])

        results = self.manager.filter_tasks_by_tag("study")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Task A")

    def test_overdue_tasks(self):
        self.manager.add_task("Old task", due_date="2000-01-01")
        self.manager.add_task("New task", due_date="2999-01-01")

        results = self.manager.get_overdue_tasks()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Old task")

    def test_stats(self):
        t1 = self.manager.add_task("Done task")
        t2 = self.manager.add_task("Pending task", due_date="2000-01-01")

        self.manager.complete_task(t1.id)

        stats = self.manager.get_stats()

        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["pending"], 1)
        self.assertEqual(stats["overdue"], 1)
        self.assertEqual(stats["completion_rate"], 50.0)


if __name__ == "__main__":
    unittest.main()