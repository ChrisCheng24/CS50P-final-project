import json
from datetime import datetime, timedelta
from plyer import notification
import schedule
import time
import sys
import multiprocessing

# Global variables
TASKS_FILE = "tasks.json"

def main():
    stop_event = multiprocessing.Event()  # Create an event for inter-process communication
    notification_process = multiprocessing.Process(target=run_notification_system, args=(stop_event,))
    notification_process.start()
    
    # Ensure the notification system starts before displaying the menu
    print("Notification system started.")
    
    try:
        while True:
            print("\n1. Add Task")
            print("2. View Tasks")
            print("3. Mark Task as Complete")
            print("4. View Task History")
            print("5. Delete Task")
            print("6. Exit")
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == "1":
                task_name = input("Enter task name: ")
                due_date = input("Enter due date (YYYY-MM-DD HH:MM): ")
                category = input("Enter category: ")
                priority = input("Enter priority (High/Medium/Low): ")
                recurrence = input("Enter recurrence (daily/weekly/monthly/none): ")
                notes = input("Enter additional notes (optional): ")
                add_task(task_name, due_date, category, priority, recurrence, notes)
            elif choice == "2":
                tasks = view_tasks()
                display_tasks(tasks)
            elif choice == "3":
                task_name = input("Enter task name to mark as complete: ")
                mark_task_completed(task_name)
            elif choice == "4":
                history = view_task_history()
                display_tasks(history, show_completed=True)
            elif choice == "5":
                task_name = input("Enter task name to delete: ")
                delete_task(task_name)
            elif choice == "6":
                print("Notifications won't be sent upon exiting, do you want to exit? (y/n)")
                stop_notifications = input().lower()

                if stop_notifications == "y":
                    print("Stopping the notification system...")
                    stop_event.set()  # Set the event to stop the notification system
                    notification_process.join()  # Wait for the notification process to terminate
                    print("Notification system terminated.")
                    print("Exiting the application.")
                    break
                else:
                    print("Returning to the main menu.")
            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nInterrupt received, stopping main application...")
    finally:
        # Ensure the notification system is stopped before exiting
        stop_event.set()
        notification_process.join()
        print("Main application closed.")
        sys.exit(0)


def add_task(task_name, due_date, category, priority, recurrence, notes=""):
    tasks = load_tasks()
    new_task = {
        "name": task_name,
        "due_date": due_date,
        "category": category,
        "priority": priority,
        "recurrence": recurrence,
        "notes": notes,
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{task_name}' added successfully!")
    return new_task

def view_tasks():
    tasks = load_tasks()
    pending_tasks = [task for task in tasks if not task["completed"]]
    return sorted(pending_tasks, key=lambda x: (x["priority"], x["due_date"]))

def mark_task_completed(task_name):
    tasks = load_tasks()
    for task in tasks:
        if task["name"] == task_name and not task["completed"]:
            task["completed"] = True
            print(f"Task '{task_name}' marked as completed!")
            
            if task["recurrence"] != "none":
                new_task = create_recurring_task(task)
                tasks.append(new_task)
                print(f"New recurring task '{new_task['name']}' added!")
            
            save_tasks(tasks)
            return tasks
    print(f"Task '{task_name}' not found or already completed.")
    return tasks

def view_task_history():
    tasks = load_tasks()
    completed_tasks = [task for task in tasks if task["completed"]]
    return sorted(completed_tasks, key=lambda x: x["due_date"], reverse=True)

def delete_task(task_name):
    tasks = load_tasks()
    initial_count = len(tasks)
    tasks = [task for task in tasks if task["name"] != task_name]
    
    if len(tasks) < initial_count:
        save_tasks(tasks)
        print(f"Task '{task_name}' deleted successfully!")
    else:
        print(f"Task '{task_name}' not found.")

def create_recurring_task(completed_task):
    new_task = completed_task.copy()
    new_task["completed"] = False
    
    due_date = datetime.strptime(completed_task["due_date"], "%Y-%m-%d %H:%M")
    if new_task["recurrence"] == "daily":
        new_due_date = due_date + timedelta(days=1)
    elif new_task["recurrence"] == "weekly":
        new_due_date = due_date + timedelta(weeks=1)
    elif new_task["recurrence"] == "monthly":
        new_due_date = due_date + timedelta(days=30)  # Approximation
    
    new_task["due_date"] = new_due_date.strftime("%Y-%m-%d %H:%M")
    return new_task

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def display_tasks(tasks, show_completed=False):
    if not tasks:
        print("No tasks to display.")
        return
    
    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        due_date = datetime.strptime(task["due_date"], "%Y-%m-%d %H:%M")
        is_overdue = due_date < datetime.now() and not task["completed"]
        print("--------------------")
        print(f"Name: {task['name']}")
        print(f"Due Date: {task['due_date']}")
        print(f"Category: {task['category']}")
        print(f"Priority: {task['priority']}")
        print(f"Status: {status}")
        if is_overdue:
            print("OVERDUE!")
        if show_completed and task["completed"]:
            print("Completed")
        print(f"Notes: {task['notes']}")
        print("--------------------")

def check_upcoming_tasks():
    tasks = view_tasks()
    now = datetime.now()
    for task in tasks:
        due_date = datetime.strptime(task["due_date"], "%Y-%m-%d %H:%M")
        time_left = due_date - now
        minutes_left = int(time_left.total_seconds() / 60)

        if 0 <= minutes_left <= 30:
            if minutes_left > 5:
                if minutes_left % 5 == 0:  # Notify every 5 minutes
                    send_notification(task, minutes_left)
            elif 0 < minutes_left <= 5:  # Notify every minute for the last 5 minutes
                send_notification(task, minutes_left)
            elif minutes_left == 0:  # Notify when time is up
                send_notification(task, 0)

def send_notification(task, minutes_left):
    if minutes_left > 0:
        message = f"{task['name']} is due in {minutes_left} minutes!"
    else:
        message = f"{task['name']} is due now!"
    
    notification.notify(
        title="Task Reminder",
        message=message,
        timeout=10
    )

def run_notification_system(stop_event):
    schedule.every(1).minutes.do(check_upcoming_tasks)
    
    while not stop_event.is_set():  # Run until the stop event is set
        schedule.run_pending()
        time.sleep(1)
    
    print("Notification system stopped.")

if __name__ == "__main__":
    main()


