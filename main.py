from manager import TaskManager
from storage import Storage
def print_banner():
    print("\n" + "=" * 60)
    print("CLI Productivity Manager")
    print("=" * 60)

def display_menu():
    print("\n===CLI Productivity Manager ===")
    print("1. Add task")
    print("2. List tasks")
    print("3. Complete task")
    print("4. Delete task")
    print("5. Search tasks by title")
    print("6. Search tasks by status")
    print("7. Filter tasks by due date")
    print("8. Filter tasks by priority")
    print("9. Filter tasks by tag")
    print("10. Sort tasks")
    print("11. Show statistics")
    print("12. Show overdue tasks")
    print("13. Exit")

def prompt_int(message):
    while True:
        raw = input(message).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid number.")

def show_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks: 
        status = "Done" if task.completed else "Pending"
        overdue = " | Overdue" if task.is_overdue() else ""
        tags = ", ".join(task.tags) if task.tags else "No tags"

        print("\n" + "-" * 60)
        print(f"ID         : {task.id}")
        print(f"Title      : {task.title}")
        print(f"Description: {task.description or 'No description'}")
        print(f"Status     : {status}{overdue}")
        print(f"Due date   : {task.due_date or 'No due date'}")
        print(f"Priority   : {task.priority}")
        print(f"Tags       : {tags}")
        print(f"Created at : {task.created_at}")
        if task.completed_at:
            print(f"Completed at: {task.completed_at}")
def show_stats(stats):
    print("\n--- Statistics ---")
    print(f"Total tasks: {stats['total']}")
    print(f"Completed tasks: {stats['completed']}")
    print(f"Pending tasks: {stats['pending']}")
    print(f"Overdue tasks: {stats['overdue']}")
    print(f"Completion rate: {stats['completion_rate']}%")



def main():
    print_banner()
    
    storage = Storage()
    manager = TaskManager()
    manager.tasks = storage.load_tasks()

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            try:
                title = input("Task title: ").strip()
                description = input("Task description: ").strip()
                due_date = input("Due date (YYYY-MM-DD, press Enter to skip): ").strip()
                priority = input("Priority (low/medium/high, press Enter for auto-suggest): ").strip()
                tags = input("Tags (comma-separated, press Enter for auto-suggest): ").strip()

                task = manager.add_task(title, description, due_date, priority, tags)
                storage.save_tasks(manager.tasks)
                print(f"Task added with ID {task.id}")
                print(f"Suggested priority: {task.priority}")
                print(f"Tags: {', '.join(task.tags) if task.tags else 'No tags'}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            show_tasks(manager.list_tasks())

        elif choice == "3":
            try:
                task_id = int(input("Enter task ID to complete: "))
                if manager.complete_task(task_id):
                    storage.save_tasks(manager.tasks)
                    print("Task marked as completed.")
                else:
                    print("Task not found.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            try:
                task_id = int(input("Enter task ID to delete: "))
                if manager.delete_task(task_id):
                    storage.save_tasks(manager.tasks)
                    print("Task deleted.")
                else:
                    print("Task not found.")
            except ValueError:
                print("Please enter a valid number.")


        elif choice == "5":
            keyword = input("Enter keyword to search: ").strip()
            results = manager.search_tasks_by_title(keyword)
            show_tasks(results)

    
        elif choice =="6":
            status = input("Enter status (completed/pending):").strip().lower()
            results = manager.search_tasks_by_status(status)

            if not results:
                print("No matching tasks found.")
            else:
                print("\nMatching tasks:")
                show_tasks(results)

        elif choice == "7":
            due_date = input("Enter due date (YYYY-MM-DD): ").strip()
            results = manager.filter_tasks_by_due_date(due_date)
            show_tasks(results)

        elif choice == "8":
            priority = input("Enter priority (low/medium/high): ").strip()
            results = manager.filter_tasks_by_priority(priority)
            show_tasks(results)

        elif choice == "9":
            tag = input("Enter tag to filter by: ").strip()
            results = manager.filter_tasks_by_tag(tag)
            show_tasks(results)

        elif choice == "10":
            print("\nSort by:")
            print("1. Newest first")
            print("2. Due date")
            print("3. Priority")
            print("4. Completed first")
            sort_choice = input("Choose sorting option: ").strip()

            sort_map = {
                "1": "newest",
                "2": "due_date",
                "3": "priority",
                "4": "completed"
            }

            sorted_tasks = manager.sort_tasks(sort_map.get(sort_choice, "newest"))
            show_tasks(sorted_tasks)

        elif choice == "11":
            stats = manager.get_stats()
            show_stats(stats)

        elif choice == "12":
            results = manager.get_overdue_tasks()
            show_tasks(results)

        elif choice == "13":
            print("Goodbye.")
            break


        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()







