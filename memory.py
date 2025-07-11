# memory.py
from langchain.memory import ConversationBufferMemory
# THIS IS THE CORRECT IMPORT PATH
from langchain_community.chat_message_histories import FileChatMessageHistory

# Point to a file where the chat history will be stored
chat_history_file = "chat_history.json"
chat_history = FileChatMessageHistory(file_path=chat_history_file)

def get_memory():
    """Returns a ConversationBufferMemory instance backed by a file."""
    return ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=chat_history,
        return_messages=True
    )