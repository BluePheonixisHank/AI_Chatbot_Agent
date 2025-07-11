from langchain.agents import initialize_agent, AgentType
from agent import get_llm
from memory import get_memory
from tools import add_todo, list_todos, remove_todo

llm = get_llm()
memory = get_memory()
tools = [add_todo, list_todos, remove_todo]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

def main():
    print("Welcome to the AI To-Do Assistant!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

        response = agent.invoke(user_input)
        print("Agent:", response)

if __name__ == "__main__":
    main()
