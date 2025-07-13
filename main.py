# main.py
from langchain.agents import initialize_agent, AgentType
from agent import get_llm
from memory import get_memory
from tools import add_todo, list_todos, smart_remove_todo, count_todos

def main():
    """Runs the main chatbot command-line interface."""
    print("Welcome to the AI To-Do Assistant!")
    print("Type 'exit' to quit.\n")
    
    llm = get_llm()
    memory = get_memory()
    # In main.py
    tools = [add_todo, list_todos, smart_remove_todo, count_todos]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        try:
            response = agent.run(user_input)
            print(f"Agent: {response}")
        except Exception as e:
            print(f"A critical error occurred: {e}")

if __name__ == "__main__":
    main()