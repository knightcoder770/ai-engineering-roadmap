import json
import os
from datetime import datetime
      
FILENAME = "todo list.json"
def load_data():
    """Loads data from the JSON file or returns an empty dict if file doesn't exist."""
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_data(data):
    """Saves the dictionary to the JSON file."""
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)

def add_task(data):
    task_id = input("give an id for the task: ")

    if task_id in data:
        print("task id already exists, choose a different id")
        return data
    name = input("enter the name of the task you want to add: ")
    assigned_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    while True:
        try:
            user_input = input("type task end date and time [YYYY-MM-DD HH:MM:SS]: ")
            valid_dt = datetime.strptime(user_input, "%Y-%m-%d %H:%M:%S")
            end_time = valid_dt.strftime("%Y-%m-%d %H:%M:%S")  # store as string for JSON
            break
        except ValueError:
            print("type date time in YYYY-MM-DD HH:MM:SS format")
            continue
    data[task_id] = {
        "name": name,
        "assigned_time": assigned_time,
        "end_time": end_time,
        "status": False
    }
    save_data(data)
    print("task added successfully")
    return data

def delete_task(data):
    task_id = input("enter the task id of the task you want to delete: ")
    if task_id in data:
        final = input("are you sure you want to delete the task? [Y/N]: ").upper()
        if final == 'Y':
            del data[task_id]
            save_data(data)
            print("task deleted successfully")
        else:
            print("deletion cancelled")
    else:
        print("task id not found")

def view_tasks(data):
    if not data:
        print("no tasks found")
        return
    print("\n" + "=" * 60)
    for task_id, details in data.items(): 
        status = "✅ done" if details["status"] else "⬜ pending"
        now = datetime.now()
        end = datetime.strptime(details["end_time"], "%Y-%m-%d %H:%M:%S")
        # deadline logic
        if details["status"]:
            deadline_msg = ""
        elif end.date() < now.date():
            deadline_msg = "❌ OVERDUE"
        elif end.date() == now.date():
            deadline_msg = "⚠️  DUE TODAY"
        else:
            days_left = (end.date() - now.date()).days
            deadline_msg = f"🕒 {days_left} days left"
        print(f"ID      : {task_id}")
        print(f"Task    : {details['name']}")
        print(f"Status  : {status}")
        print(f"Created : {details['assigned_time']}")
        print(f"Deadline: {details['end_time']}  {deadline_msg}")
        print("-" * 60)

def view_completed_tasks(data):
    completed = {k: v for k, v in data.items() if v["status"]}
    if not completed:
        print("no completed tasks found")
        return
    print("\n--- COMPLETED TASKS ---")
    view_tasks(completed)

def view_pending_tasks(data):
    pending = {k: v for k, v in data.items() if not v["status"]}
    if not pending:
        print("no pending tasks found")
        return
    print("\n--- PENDING TASKS ---")
    view_tasks(pending)

def complete_task(data):
    task_id = input("enter the task id to mark as complete: ")
    if task_id in data:
        data[task_id]["status"] = True
        save_data(data)
        print("task marked as complete")
    else:
        print("task id not found")

def main():
    data = load_data()  # load once at start, not empty dict
    print("your to do list")
    while True:
        try:
            print("\n1-ADD TASK\n2-DELETE TASK\n3-VIEW ALL TASKS\n4-VIEW COMPLETED TASKS\n5-VIEW PENDING TASKS\n6-MARK TASK COMPLETE\n7-EXIT")
            opinion = int(input("CHOOSE THE OPTION NO YOU ARE INTERESTED IN: "))
            if opinion not in range(1, 8):
                print("choose only the option number [1-7]")
                continue
        except ValueError:
            print("you must only choose the option number [1-7]")
            continue
        if opinion == 1:
            data = add_task(data)
        elif opinion == 2:
            delete_task(data)
        elif opinion == 3:
            view_tasks(data)
        elif opinion == 4:
            view_completed_tasks(data)
        elif opinion == 5:
            view_pending_tasks(data)
        elif opinion == 6:
            complete_task(data)
        else:
            break

if __name__ == "__main__":
    main()