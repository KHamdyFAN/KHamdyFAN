import json
import os
import hashlib

USERS_FILE = "data/users.json"
TASKS_FILE = "data/tasks.json"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return {}


def authenticate_user(username, password):
    users = load_users()
    return users.get(username) == hash_password(password)


def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = hash_password(password)
    with open(USERS_FILE, "w") as file:
        json.dump(users, file)
    return True


def load_tasks(username):
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r") as file:
                tasks = json.load(file)
            # If tasks is a list, convert it to a dictionary
            if isinstance(tasks, list):
                print("Warning: Incorrect format detected, resetting tasks to proper structure.")
                tasks = {}
                with open(TASKS_FILE, "w") as file:
                    json.dump(tasks, file)
            return tasks.get(username, [])
        except json.JSONDecodeError:
            return []
    return []


def save_tasks(username, tasks):
    all_tasks = {}
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            all_tasks = json.load(file)
    all_tasks[username] = tasks
    with open(TASKS_FILE, "w") as file:
        json.dump(all_tasks, file)
