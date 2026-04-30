from smart_rules import suggest_priority, suggest_tags
from datetime import datetime,date
from task import Task

class TaskManager:
    validate_priority ={"low", "medium", "high"}
    def __init__(self):
        self.tasks =[]

    def _validate_title(self,title):
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        return title

    def _validate_due_date(self, due_date):
        due_date = due_date.strip()
        if not due_date :
            return ""
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format.")
        return due_date
    
    def _validate_priority(self, priority):
        priority = (priority or"medium").strip().lower()
        if priority not in self.validate_priority:
            raise ValueError("Priority must be in low, medium, or high.")
        return priority
    
    def _normalize_tags(self, tags):
        if tags is None:
            return []

        if isinstance(tags, str):
            tags = tags.split(",")

        return [tag.strip().lower() for tag in tags if tag.strip()]
    
    def _parse_created_at(self, value):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return datetime.min

    def _parse_due_date(self, value):
        if not value:
            return date.max
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return date.max    

    def add_task(self, title, description="", due_date="", priority="", tags=None):
        title = self._validate_title(title)
        due_date = self._validate_due_date(due_date)

        if not priority:
            priority = suggest_priority(title, description)
        priority = self._validate_priority(priority)

        if not tags:
            tags = suggest_tags(title, description)
        tags = self._normalize_tags(tags)

        task_id = 1 if not self.tasks else max(task.id for task in self.tasks) + 1
        task = Task(
            id=task_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            tags=tags
        )
        self.tasks.append(task)
        return task
    
    def list_tasks(self):
        return self.tasks

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id ==task_id:
                return task
        return None
        
    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False
   
    def complete_task(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_completed()
            return True
        return False
    
    
    def search_tasks_by_title(self, keyword):
        keyword = keyword.lower()
        return [task for task in self.tasks if keyword in task.title.lower()]
    
    def search_tasks_by_status(self, status):
        status = status.lower() 

        if status == "completed":
            return[task for task in self.tasks if task.completed] 
        elif status == "pending":
            return[task for task in self.tasks if not task.completed] 
        else:
            return []

    def filter_tasks_by_due_date(self, due_date):
        due_date = due_date.strip()
        return [task for task in self.tasks if task.due_date == due_date]
    
    def filter_tasks_by_priority(self, priority):
        priority = priority.lower().strip()
        return [task for task in self.tasks if task.priority == priority]
    
    def get_overdue_tasks(self):
        return [task for task in self.tasks if task.is_overdue()]    


    def filter_tasks_by_tag(self, tag):
        tag = tag.lower().strip()
        return [task for task in self.tasks if tag in task.tags]



    def sort_tasks(self, sort_by="newest"):
        if sort_by == "newest":
            return sorted(
                self.tasks,
                key=lambda task: self._parse_created_at(task.created_at),
                reverse=True
            )

        if sort_by == "due_date":
            return sorted(
                self.tasks,
                key=lambda task: self._parse_due_date(task.due_date)
            )

        if sort_by == "priority":
            order = {"high": 3, "medium": 2, "low": 1}
            return sorted(
                self.tasks,
                key=lambda task: order.get(task.priority, 2),
                reverse=True
            )

        if sort_by == "completed":
            return sorted(
                self.tasks,
                key=lambda task: (not task.completed, self._parse_created_at(task.created_at))
            )

        return self.tasks

    def get_stats(self):
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        pending = total - completed
        overdue = sum(1 for task in self.tasks if task.is_overdue())
        completion_rate = round((completed / total) * 100, 2) if total else 0.0

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue,
            "completion_rate": completion_rate
        }