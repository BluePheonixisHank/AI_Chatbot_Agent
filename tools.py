# tools.py
import json
from langchain_core.tools import tool
from typing import List

TODO_FILE = "todos.json"

def read_todos() -> List[str]:
    """Reads the to-do list from the JSON file."""
    try:
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def write_todos(todos: List[str]):
    """Writes the to-do list to the JSON file."""
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=4)

@tool
def add_todo(item: str) -> str:
    """
    Adds a new item to the user's to-do list.
    Use this when the user wants to add a task or a to-do.
    """
    todos = read_todos()
    if item not in todos:
        todos.append(item)
        write_todos(todos)
        return f"Successfully added '{item}' to your to-do list."
    return f"'{item}' is already on your to-do list."

@tool
def list_todos(dummy_arg: str = "") -> List[str]:
    """
    Lists all the items on the user's to-do list.
    Use this when the user wants to see their to-do list.
    """
    return read_todos()

@tool
def remove_todo(item: str) -> str:
    """
    Removes an item from the user's to-do list.
    Use this when the user wants to remove or delete a task.
    """
    todos = read_todos()
    if item in todos:
        todos.remove(item)
        write_todos(todos)
        return f"Successfully removed '{item}' from your to-do list."
    return f"Could not find '{item}' on your to-do list."