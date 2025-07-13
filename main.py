# main.py
from langchain.agents import initialize_agent, AgentType
from agent import get_llm
from memory import get_memory
from tools import add_todo, list_todos, remove_todo, smart_remove_todo

def main():
    """Runs the main chatbot command-line interface."""
    print("Welcome to the AI To-Do Assistant!")
    print("Type 'exit' to quit.\n")
    
    llm = get_llm()
    memory = get_memory()
    tools = [smart_remove_todo, add_todo, list_todos, remove_todo]

    # Initialize the agent using the stable AgentExecutor
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True  # Set to False for a cleaner output
    )

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        try:
            # The agent returns a dictionary, we are interested in the 'output' key
            response = agent.run(user_input)
            print(f"Agent: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()