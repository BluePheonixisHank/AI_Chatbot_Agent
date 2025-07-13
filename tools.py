# tools.py
import json
from langchain_core.tools import tool
from typing import List

TODO_FILE = "todos.json"

def read_todos() -> List[str]:
    """Reads the list of to-do strings from the JSON file."""
    try:
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_todos(todos: List[str]):
    """Writes the list of to-do strings to the JSON file."""
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=4)

@tool
def add_todo(item: str) -> str:
    """
    Adds a new, specific item to the user's to-do list.
    Use this when the user is creating a new task.
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
    Lists all items on the user's to-do list. Returns a single, formatted string.
    """
    todos = read_todos()
    if not todos:
        return "Your to-do list is empty."
    formatted_list = "\n".join(f"- {item}" for item in todos)
    return formatted_list

@tool
def smart_remove_todo(user_query: str) -> str:
    """
    Intelligently removes a to-do item based on a user's description.
    This tool finds the best match from the existing tasks and removes it.
    """
    todos = read_todos()
    if not todos:
        return "The to-do list is already empty."

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from agent import get_llm

    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        "Given the user's request: '{query}', which of the following tasks is the single best match?:\n\n{task_list}\n\nOnly return the exact text of the best matching task. If no items are a good match, return the word 'NONE'."
    )
    chain = prompt | llm | StrOutputParser()
    
    best_match = chain.invoke({
        "query": user_query,
        "task_list": "\n".join(f"- {name}" for name in todos)
    })

    if best_match == "NONE" or best_match not in todos:
        return f"Sorry, I couldn't find a matching task for '{user_query}'."
    else:
        todos.remove(best_match)
        write_todos(todos)
        return f"Successfully removed '{best_match}' from your to-do list."
    

@tool
def count_todos(dummy_arg: str = "") -> str:
    """
    Counts the number of items currently on the to-do list and returns a descriptive string.
    Use this when the user asks 'how many tasks do I have?' or similar questions.
    """
    todos = read_todos()
    count = len(todos)
    if count == 0:
        return "You have no tasks on your to-do list."
    elif count == 1:
        return "You have 1 task on your to-do list."
    else:
        return f"You have {count} tasks on your to-do list."