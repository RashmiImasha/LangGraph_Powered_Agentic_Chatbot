from backend import chatbot, get_all_threads
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
import streamlit as st
import uuid

# generate unique thread id for each session
def generate_thread_id():
    return str(uuid.uuid4())

# add new thread id
def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def reset_chat():
    st.session_state['thread_id'] = generate_thread_id()
    # Clear the current chat messages from the UI
    st.session_state['message_history'] = []
    
    add_thread(st.session_state['thread_id'])

# Load a previous conversation from the LangGraph checkpointer
def load_chat(thread_id):

    # Get the saved state for the selected thread
    state = chatbot.get_state(
        config={'configurable': {'thread_id': thread_id}}
    )

    return state.values.get('messages', [])

st.title("Agentic Chatbot with Langgraph")

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
    

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = get_all_threads()

# Add current thread to the chat list
add_thread(st.session_state['thread_id'])


# ************Sidebar threading feature**************

st.sidebar.title("My Chats")

if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()

# Display all conversation threads in reverse order
for thread_id in st.session_state['chat_threads'][::-1]:

    # Create one sidebar button for every conversation
    if st.sidebar.button(
        str(thread_id), 
        key=thread_id
    ):
        
        st.session_state['thread_id'] = thread_id
        # Load the message history for the selected thread
        messages = load_chat(thread_id)

        # Temporary list for converting LangChain messages
        # into Streamlit's required message format
        temp_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            elif isinstance(message, AIMessage):
                role = 'assistant'
            else: 
                continue    # Ignore other message types, such as ToolMessage
            
            temp_messages.append(
                {'role': role, 'content': message.content}
            )
        
        st.session_state['message_history'] = temp_messages
        st.rerun()


# ========================= Main chat interface =========================

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
        
user_input = st.chat_input("Type here")

# first add the message to message_history
if user_input:

    st.session_state['message_history'].append({'role': 'user', 'content': user_input})

    # display user's message
    with st.chat_message('user'):
        st.text(user_input)

    # Pass the current thread ID to LangGraph
    # LangGraph uses this ID to save and retrieve conversation memory
    config = {'configurable': {'thread_id': st.session_state['thread_id']}}


    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]}, 
                config=config,
                stream_mode='messages'
            )
            
            # Display only AI messages
            # This prevents tool and user messages from appearing
            if isinstance(message_chunk, AIMessage)        
        )

       
            
    # Save the complete assistant response in Streamlit session state
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    







