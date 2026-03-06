#!/usr/bin/env python3
"""
What-a-Gwan: A simple task tracker CLI.
Track what's going on with your tasks.
"""

import json
import os
import sys
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


def load_tasks():
    """Load tasks from the JSON data file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    """Save tasks to the JSON data file."""
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(title, priority="medium"):
    """Add a new task."""
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority,
        "done": False,
        "created_at": datetime.now().isoformat(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {title}")


def list_tasks(show_all=False):
    """List tasks. By default only shows incomplete tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet. Add one with: python task_tracker.py add <title>")
        return

    # TODO: Add filtering by priority (e.g. --priority high)
    displayed = [t for t in tasks if show_all or not t["done"]]
    if not displayed:
        print("All tasks are done! 🎉")
        return

    for task in displayed:
        status = "✓" if task["done"] else " "
        # TODO: Add color output for different priority levels
        completed_info = ""
        if task["done"] and "completed_at" in task:
            completed_info = f" (completed {task['completed_at'][:10]})"
        print(f"  [{status}] #{task['id']} ({task['priority']}) {task['title']}{completed_info}")


def complete_task(task_id):
    """Mark a task as completed."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            task["completed_at"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Completed task #{task_id}: {task['title']}")
            return
    print(f"Task #{task_id} not found.")


def delete_task(task_id):
    """Delete a task by ID."""
    tasks = load_tasks()
    original_len = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == original_len:
        print(f"Task #{task_id} not found.")
        return
    save_tasks(tasks)
    print(f"Deleted task #{task_id}")


def show_summary():
    """Show a summary of task counts."""
    tasks = load_tasks()
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    pending = total - done
    # TODO: Show breakdown by priority in the summary
    print(f"Total: {total} | Done: {done} | Pending: {pending}")


def print_usage():
    print("What-a-Gwan Task Tracker")
    print()
    print("Usage:")
    print("  python task_tracker.py add <title> [--priority high|medium|low]")
    print("  python task_tracker.py list [--all]")
    print("  python task_tracker.py done <id>")
    print("  python task_tracker.py delete <id>")
    print("  python task_tracker.py summary")


def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: task title required.")
            return
        priority = "medium"
        title_parts = []
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--priority" and i + 1 < len(sys.argv):
                priority = sys.argv[i + 1]
                i += 2
            else:
                title_parts.append(sys.argv[i])
                i += 1
        add_task(" ".join(title_parts), priority)

    elif command == "list":
        show_all = "--all" in sys.argv
        list_tasks(show_all)

    elif command == "done":
        if len(sys.argv) < 3:
            print("Error: task ID required.")
            return
        complete_task(int(sys.argv[2]))

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: task ID required.")
            return
        delete_task(int(sys.argv[2]))

    elif command == "summary":
        show_summary()

    else:
        print(f"Unknown command: {command}")
        print_usage()


if __name__ == "__main__":
    main()
