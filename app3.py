import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Page config
st.set_page_config(page_title="Llama3 Chatbot", page_icon="🦙")
st.title("🦙 Llama3 Chatbot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Load Llama3 (cached to avoid reloading)
@st.cache_resource
def load_llm():
    try:
        return Ollama(model="llama3")
    except Exception as e:
        st.error(f"Failed to load Llama3: {e}")
        st.info("Make sure Ollama is installed and running, and you've run: ollama pull llama3")
        return None

llm = load_llm()

# Only proceed if LLM loaded successfully
if llm is not None:
    # Create chain
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful, respectful, and honest AI assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])
    chain = prompt | llm

    # Display chat history
    for msg in st.session_state.chat_history:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)

    # User input
    if user_input := st.chat_input("Ask something..."):
        # Add user message
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Llama3 is thinking..."):
                try:
                    response = chain.invoke({
                        "input": user_input,
                        "chat_history": st.session_state.chat_history[:-1]  # exclude current msg
                    })
                    st.markdown(response)
                    st.session_state.chat_history.append(AIMessage(content=response))
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.info("Check if Ollama is running and Llama3 is downloaded.")
else:
    st.warning("Llama3 model not available. Please check setup instructions.")