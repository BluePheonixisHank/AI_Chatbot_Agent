# tools.py
import json
from langchain.tools import tool
from typing import List

# Define the file path for our persistent to-do list
TODO_FILE = "todos.json"

def read_todos() -> List[str]:
    """A helper function to read the to-do list from the JSON file."""
    try:
        with open(TODO_FILE, 'r') as f:
            # Handle the case where the file might be empty
            content = f.read()
            if not content:
                return []
            return json.loads(content)
    except FileNotFoundError:
        # If the file doesn't exist yet, start with an empty list
        return []

def write_todos(todos: List[str]):
    """A helper function to write the entire to-do list to the JSON file."""
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=4)

@tool
def add_todo(item: str) -> str:
    """
    Adds a new item to the user's to-do list. Use this when a user wants to add a task.
    For example: 'add "buy milk" to my to-do list'
    """
    todos = read_todos() # Read the current list from the file
    if item not in todos:
        todos.append(item)
        write_todos(todos) # Write the updated list back to the file
        return f'Successfully added "{item}" to your to-do list.'
    return f'"{item}" is already on your to-do list.'

@tool
def list_todos(dummy_input: str = "") -> str:
    """Lists all the items on the user's to-do list."""
    todos = read_todos() # Always read the latest list from the file
    if not todos:
        return "Your to-do list is empty."
    # Format the list with bullet points for better readability
    return "\n".join(f"- {item}" for item in todos)

@tool
def remove_todo(item: str) -> str:
    """
    Removes an item from the user's to-do list by its exact name. Use this when a user wants to delete or complete a task.
    """
    todos = read_todos() # Read from the file
    if item in todos:
        todos.remove(item)
        write_todos(todos) # Write the changes back to the file
        return f'Successfully removed "{item}" from your to-do list.'
    return f'Could not find "{item}" on your to-do list.'