import json
from pathlib import Path
from task import Task

class Storage:
    def __init__(self, file_path ="data/tasks.json"):
        self.file_path = Path(file_path)

    def save_tasks(self, tasks):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=4)
    
    def load_tasks(self):
        if not self.file_path.exists():
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return[Task.from_dict(item) for item in data]
        except json.JSONDecodeError:
            print("Wearning : Corrupted JSON, resetting file.")
            return []
        except OSError as e:
            print(f"File error: {e}")
            return []
   


