# AI To-Do List Agent

This project is a conversational AI agent designed to act as a personal assistant. It can hold a conversation, remember context, and manage a persistent to-do list for the user. The project is built using Python, LangChain, and the Google Gemini API.



## Current State: Persistent Memory Implemented

As of the latest commit, the agent has the following core features:
*   **Conversational Ability**: Can chat with a user.
*   **Persistent To-Do List**: The to-do list is saved to a `todos.json` file and is reloaded when the agent restarts.
*   **Persistent Chat History**: The conversation history is saved to a `chat_history.json` file, allowing the agent to remember the context of previous conversations (e.g., the user's name).

## Architecture

The agent is currently built using the standard LangChain `AgentExecutor`. This architecture follows the **ReAct (Reasoning and Acting)** model, where the Language Model can reason about a user's request and choose to act by using a set of predefined tools.

The key components are:

1.  **LLM (Language Model)**: **Google Gemini 1.5 Flash** is used as the "brain" of the agent to drive conversation and make decisions.
2.  **Tools**: These are Python functions (`add_todo`, `list_todos`, `remove_todo`) that the agent can execute to interact with the to-do list stored on the file system.
3.  **Memory**: `ConversationBufferMemory` is used to store the history of the conversation. This memory is explicitly configured to be persistent.
4.  **Agent Executor**: The main engine from LangChain (`initialize_agent`) that orchestrates the interaction between the LLM, Memory, and Tools.

### Flow Description

```mermaid
graph TD
    A[User Input] --> B[Agent Executor];
    B --sends prompt with history--> C[LLM (Gemini)];
    C --accesses context from--> D[Memory (chat_history.json)];
    C --"I should use a tool"--> E{Tool Call?};
    E --Yes--> F[Execute Tool e.g., add_todo];
    F --reads/writes--> G[Storage (todos.json)];
    F --returns result--> B;
    B --sends tool result back to--> C;
    C --"I now have the answer"--> E;
    E --No, generate final response--> H[AI Response];
    H --> I[Output to User];
```

## How Memory is Stored and Retrieved

Persistence is handled using simple JSON files, making the agent stateful across sessions.

*   **Conversation History**: We use LangChain's `FileChatMessageHistory` (from `langchain_community.chat_message_histories`) configured in `memory.py`. This class automatically saves the entire conversation to `chat_history.json` and loads it back when the agent starts.

*   **To-Do List**: The to-do list is stored in `todos.json`. The tool functions in `tools.py` are responsible for all file interactions. They follow a clear **read-modify-write** pattern: they read the current list from the file, modify it in memory, and then write the entire updated list back to the file.

## How Tool Calls are Defined and Registered

*   **Definition**: Each tool is a Python function in `tools.py` decorated with the **`@tool`** decorator. The function's docstring serves as the description that the LLM uses to decide when to call it.

*   **Registration**: In `main.py`, the tool functions are collected into a `tools` list. This list is passed directly to the `initialize_agent` function, making the agent aware of the actions it can perform.

## Setup and Run Instructions

1.  **Clone the Repository**
    ```bash
    git clone git@github.com:BluePheonixisHank/AI_Chatbot_Agent.git
    cd AI_Chatbot_Agent
    ```

2.  **Create a Virtual Environment**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up API Key**
    *   Create a file named `.env` in the project root.
    *   Add your Google AI Studio API key to the file:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

5.  **Run the Chatbot**
    ```bash
    python main.py
    ```

## Limitations and Next Steps

*   **API Rate Limiting**: The Google AI free tier has a daily request limit (e.g., 50 calls/day). Extensive testing can exhaust this quota.
*   **Single-User**: The current file-based persistence is not suitable for multiple users.
*   **Next Major Step**: The current `AgentExecutor` is functional but will be deprecated. The next step is to refactor the entire architecture to use **LangGraph**, which provides a more robust, explicit, and modern way to build agentic systems, as recommended by the LangChain team and the assignment prompt.