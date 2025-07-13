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
    Adds a new, specific item to the user's to-do list. Use this when the user is creating a new task.
    For example: 'add "buy milk" to my to-do list'
    """
    todos = read_todos()
    if item not in todos:
        todos.append(item)
        write_todos(todos)
        return f"Successfully added '{item}' to your to-do list."
    return f"'{item}' is already on your to-do list."

@tool
def list_todos(dummy_arg: str = "") -> str:
    """
    Lists all the items on the user's to-do list. Returns a single, formatted string.
    Use this when the user wants to see their current tasks.
    """
    todos = read_todos()
    if not todos:
        return "Your to-do list is empty."
    
    # Format the list into a clean, human-readable string with newlines
    # This is what the LLM can easily understand and present.
    formatted_list = "\n".join(f"- {item}" for item in todos)
    return formatted_list

# We keep the original remove_todo tool as a fallback, but we remove its docstring
# so the LLM doesn't see it as a primary option.
@tool
def remove_todo(item: str) -> str:
    """Removes an item by exact name. This tool is for internal use and should not be called directly by the LLM unless the new smart_remove_todo tool fails."""
    todos = read_todos()
    if item in todos:
        todos.remove(item)
        write_todos(todos)
        return f"Successfully removed '{item}' from your to-do list."
    return f"Could not find '{item}' on your to-do list."

# This is our new, intelligent tool!
@tool
def smart_remove_todo(user_query: str) -> str:
    """
    Intelligently removes a to-do item based on a user's potentially vague description.
    Use this tool FIRST when a user wants to remove, delete, or complete a task.
    This tool will find the best match from the existing to-do list and remove it.
    For example, if the user says 'I'm done with the tutorial', this tool should be used.
    The input should be the user's original phrase for what they want to remove.
    """
    todos = read_todos()
    if not todos:
        return "The to-do list is already empty."

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from agent import get_llm # We import this locally to avoid circular dependencies

    # Create a small, temporary chain to ask the LLM for the best match
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        "Given the user's request: '{query}', which of the following to-do items is the best match?:\n\n{todo_list}\n\nOnly return the single, exact to-do item text that is the best match. If no items are a good match, return the word 'NONE'."
    )
    
    # Chain the components together
    chain = prompt | llm | StrOutputParser()
    
    # Ask the LLM to find the best match
    best_match = chain.invoke({
        "query": user_query,
        "todo_list": "\n".join(f"- {t}" for t in todos)
    })

    if best_match == "NONE" or best_match not in todos:
        return f"Sorry, I couldn't find a matching to-do item for '{user_query}'."
    else:
        # If we found a match, call our original, simple remove_todo tool
        return remove_todo(best_match)