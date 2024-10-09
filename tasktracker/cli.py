import argparse
from tasktracker.taskl import TaskTracker

def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    parser.add_argument("action", choices=["add", "list", "delete", "done", "inactive"], help="Action to perform")
    parser.add_argument("--title", help="Title of the task")
    parser.add_argument("--description", help="Description of the task")

    args = parser.parse_args()
    tracker = TaskTracker()  # Create an instance of TaskTracker that loads tasks from JSON

    if args.action == "add":
        if args.title and args.description:
            tracker.add_task(args.title, args.description)
            print(f"Task '{args.title}' added successfully.")
        else:
            print("Please provide both title and description for the new task.")
    elif args.action == "list":
        tasks = tracker.list_tasks()
        if tasks:
            for task in tasks:
                print(task)
        else:
            print("No tasks found.")
    elif args.action == "delete":
        if args.title:
            tracker.delete_task(args.title)
            print(f"Task '{args.title}' deleted successfully.")
        else:
            print("Please provide the title of the task to delete.")
    elif args.action == "done":
        if args.title:
            tracker.mark_task_done(args.title)
            print(f"Task '{args.title}' marked as done.")
        else:
            print("Please provide the title of the task to mark as done.")
    elif args.action == "inactive":
        if args.title:
            tracker.mark_task_inactive(args.title)
            print(f"Task '{args.title}' marked as inactive.")
        else:
            print("Please provide the title of the task to mark as inactive.")

if __name__ == "__main__":
    main()
