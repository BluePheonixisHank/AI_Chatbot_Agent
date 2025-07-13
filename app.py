# app.py
import streamlit as st
from langchain.agents import initialize_agent, AgentType
from agent import get_llm
from memory import get_memory
from tools import add_todo, list_todos, smart_remove_todo, count_todos

# --- Page Configuration ---
st.set_page_config(
    page_title="Agentic AI To-Do Assistant",
    page_icon="✅",
    layout="wide"
)

# --- Agent Initialization ---
# We create a function to initialize the agent so we can cache it.
# Caching prevents the agent from being re-created on every interaction.
@st.cache_resource
def get_agent():
    """Initializes and returns the LangChain agent."""
    print("Initializing agent...")
    llm = get_llm()
    memory = get_memory()
    tools = [add_todo, list_todos, smart_remove_todo, count_todos]
    
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        # Set verbose to False for a cleaner UI experience
        verbose=False,
        handle_parsing_errors=True
    )

# --- App Layout and Logic ---
st.title("✅ Agentic AI To-Do Assistant")
st.write("Welcome! I'm your personal assistant. I can chat with you and manage your to-do list.")

# Initialize or retrieve the agent from the cache
agent = get_agent()

# Initialize chat history in Streamlit's session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What would you like to do?"):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get the assistant's response
    with st.spinner("Thinking..."):
        try:
            # We use st.session_state to make sure memory persists across reruns
            # The agent's own file-based memory will handle the long-term persistence.
            response = agent.run(prompt)
            
            # Add assistant response to session state and display it
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)

        except Exception as e:
            error_message = f"Sorry, an error occurred: {e}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            with st.chat_message("assistant"):
                st.markdown(error_message)