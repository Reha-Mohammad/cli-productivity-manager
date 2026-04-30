#  CLI Productivity Manager

A Python command-line productivity app for managing tasks in a clean and practical way.

## Features

* Add tasks
* List tasks
* Complete tasks
* Delete tasks
* Search tasks by title
* Search tasks by status
* Filter tasks by due date
* Filter tasks by priority
* Filter tasks by tag
* Show overdue tasks
* Sort tasks by newest, due date, priority, or completion
* Show productivity statistics
* Save and load tasks from a JSON file
* Auto-suggest priority and tags from task content

## Why this project exists

This project was built to practice:

* Python classes and objects
* file handling with JSON
* modular project structure
* validation and error handling
* command-line application design
* testing
* GitHub project organization

## Project Structure

```text
cli_productivity_manager/
├── main.py
├── task.py
├── manager.py
├── storage.py
├── smart_rules.py
├── data/
│   └── tasks.json
├── tests/
│   ├── test_task_manager.py
│   └── test_storage.py
└── README.md
```

## Requirements

* Python 3.10 or newer

## How to Run

1. Clone the repository
2. Open the project folder
3. Run:

```bash
python main.py
```

## How to Run Tests

Run the test suite with:

```bash
python -m unittest discover -s tests
```

## Example Menu

```text
1. Add task
2. List tasks
3. Complete task
4. Delete task
5. Search tasks by title
6. Search tasks by status
7. Filter tasks by due date
8. Filter tasks by priority
9. Filter tasks by tag
10. Sort tasks
11. Show statistics
12. Show overdue tasks
13. Exit
```

## Example Task

* Title: Finish thesis chapter
* Description: Draft the introduction section
* Due date: 2026-05-01
* Priority: high
* Tags: thesis, study


## Notes

This is a learning and portfolio project focused on clean code, structure, and practical Python development.
