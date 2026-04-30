def suggest_priority(title, description=""):
    text = f"{title} {description}".lower()

    high_keywords = [
        "urgent", "asap", "deadline", "thesis", "exam", "interview",
        "submit", "final", "important", "critical"
    ]

    medium_keywords = [
        "study", "prepare", "review", "write", "update", "fix", "meeting"
    ]

    if any(word in text for word in high_keywords):
        return "high"
    if any(word in text for word in medium_keywords):
        return "medium"
    return "low"


def suggest_tags(title, description=""):
    text = f"{title} {description}".lower()
    tags = []

    rules = {
        "study": ["study", "learn", "course", "exam", "lecture", "python", "django"],
        "work": ["work", "project", "meeting", "report", "client", "deadline"],
        "personal": ["buy", "groceries", "home", "family", "doctor", "pay"],
        "thesis": ["thesis", "research", "paper", "journal", "review", "manuscript"],
    }

    for tag, keywords in rules.items():
        if any(word in text for word in keywords):
            tags.append(tag)

    return tags