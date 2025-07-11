from langchain.tools import tool

todos = []

@tool
def add_todo(item: str) -> str:
    """Adds a to-do item."""
    todos.append(item)
    return f'Added "{item}" to your to-do list.'

@tool
def list_todos(dummy_input: str) -> str:
    """Lists all current to-do items."""
    if not todos:
        return "Your to-do list is empty."
    return "\n".join(f"{i+1}. {item}" for i, item in enumerate(todos))

@tool
def remove_todo(item: str) -> str:
    """Removes a to-do item by exact name."""
    if item in todos:
        todos.remove(item)
        return f'Removed "{item}" from your to-do list.'
    return f'"{item}" not found in your to-do list.'
