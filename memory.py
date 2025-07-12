# memory.py
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory

def get_memory():
    """Returns a ConversationBufferMemory instance with file-based history."""
    # Use a file to store chat history. This provides persistence between sessions.
    chat_history = FileChatMessageHistory(file_path="chat_history.json")
    
    return ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=chat_history,
        return_messages=True
    )