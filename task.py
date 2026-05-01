from dataclasses import dataclass, asdict,field
from datetime import datetime

# This is your first real object-oriented class in a project:
@dataclass
class Task:
    id: int 
    title: str
    description : str = ""
    due_date: str = ""       # example: "2026-05-01"
    priority: str = "medium"
    tags: list[str] = field(default_factory=list)
    completed: bool = False
    created_at: str = "" 
    completed_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat(timespec="seconds")
        self.title = self.title.strip()
        self.description = self.description.strip()
        self.due_date = self.due_date.strip()
        self.priority = (self.priority or "medium").strip().lower() 
        
        if self.priority:
            self.priority = self.priority.lower()
        else:
            self.priority = "medium"
        self.tags = [tag.strip().lower() for tag in self.tags if tag and tag.strip()]

        if self.completed_at:
            self.completed_at = self.completed_at.strip()

    def mark_completed(self):
        self.completed = True
        self.completed_at = datetime.now().isoformat(timespec="seconds")


    def is_overdue(self):
        if not self.due_date or self.completed:
            return False
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            return today > due
        except ValueError:
            return False

    def to_dict(self):
        return asdict(self)
    
    @staticmethod
    def from_dict(data):
        raw_tags = data.get("tags", [])
        if isinstance(raw_tags, str):
            raw_tags = [tag.strip() for tag in raw_tags.split(",") if tag.strip()]
        return Task(
            id = data["id"],
            title = data["title"],
            description= data.get("description",""),
            due_date = data.get("due_date", ""),
            priority=data.get("priority", "medium"),
            tags=raw_tags,
            completed = data.get("completed", False),
            created_at = data.get("created_at", ""),
            completed_at=data.get("completed_at", "")
        )
