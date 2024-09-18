import pytest
import json
from datetime import datetime, timedelta
from project import (
    add_task, 
    view_tasks, 
    mark_task_completed, 
    view_task_history, 
    delete_task, 
    create_recurring_task, 
    load_tasks, 
    save_tasks
)

TASKS_FILE = "tasks.json"

# Helper function to reset tasks file before tests
def reset_tasks_file():
    with open(TASKS_FILE, "w") as file:
        json.dump([], file)

@pytest.fixture(autouse=True)
def setup_tasks_file():
    """Fixture to ensure tasks file is reset before each test."""
    reset_tasks_file()
    yield
    reset_tasks_file()

# Test for add_task function
def test_add_task():
    task_name = "Test Task"
    due_date = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
    category = "Test"
    priority = "High"
    recurrence = "none"
    notes = "This is a test task."
    
    added_task = add_task(task_name, due_date, category, priority, recurrence, notes)
    
    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0] == added_task
    assert tasks[0]["name"] == task_name
    assert tasks[0]["due_date"] == due_date
    assert tasks[0]["category"] == category
    assert tasks[0]["priority"] == priority
    assert tasks[0]["recurrence"] == recurrence
    assert tasks[0]["notes"] == notes

# Test for view_tasks function
def test_view_tasks():
    # Add some tasks
    add_task("Task 1", "2024-09-11 12:00", "Work", "Medium", "none", "")
    add_task("Task 2", "2024-09-11 14:00", "Personal", "High", "none", "")
    
    tasks = view_tasks()
    assert len(tasks) == 2
    assert tasks[0]["name"] == "Task 2"  # High priority comes first
    assert tasks[1]["name"] == "Task 1"

# Test for mark_task_completed function
def test_mark_task_completed():
    task_name = "Task to Complete"
    add_task(task_name, "2024-09-12 10:00", "Work", "Low", "none", "")
    
    mark_task_completed(task_name)
    
    tasks = load_tasks()
    completed_task = next(task for task in tasks if task["name"] == task_name)
    assert completed_task["completed"] is True

# Test for view_task_history function
def test_view_task_history():
    add_task("Task 1", "2024-09-11 12:00", "Work", "Low", "none", "")
    add_task("Task 2", "2024-09-11 14:00", "Personal", "Medium", "none", "")
    
    mark_task_completed("Task 1")
    
    history = view_task_history()
    assert len(history) == 1
    assert history[0]["name"] == "Task 1"
    assert history[0]["completed"] is True

# Test for delete_task function
def test_delete_task():
    task_name = "Task to Delete"
    add_task(task_name, "2024-09-12 10:00", "Work", "Low", "none", "")
    
    delete_task(task_name)
    
    tasks = load_tasks()
    assert not any(task["name"] == task_name for task in tasks)

# Test for create_recurring_task function
def test_create_recurring_task():
    original_task = {
        "name": "Recurring Task",
        "due_date": (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
        "category": "Work",
        "priority": "Medium",
        "recurrence": "daily",
        "notes": "",
        "completed": True
    }
    
    new_task = create_recurring_task(original_task)
    
    assert new_task["name"] == original_task["name"]
    assert new_task["completed"] is False
    assert new_task["recurrence"] == "daily"
    
    original_due_date = datetime.strptime(original_task["due_date"], "%Y-%m-%d %H:%M")
    new_due_date = datetime.strptime(new_task["due_date"], "%Y-%m-%d %H:%M")
    
    assert new_due_date == original_due_date + timedelta(days=1)








