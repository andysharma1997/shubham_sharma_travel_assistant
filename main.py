import streamlit as st
from dotenv import load_dotenv
from app.services.travel_agent import SmartTravelAgent
from app.services.agent_tools.implementation.search_tool import SearchTool
from app.utilities.constants import Constants

search_tool = SearchTool()
travel_agent = SmartTravelAgent(tools=[search_tool.get_tool()])

system_prompt= Constants.fetch_constant("system_prompt")

st.set_page_config(page_title="Travel Chatbot", page_icon="🌍")

st.title("🌍 Smart Agentic Travel Bot")

# Initialize conversation history in session state if it doesn't exist
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Reset conversation
if st.button("🔄 Reset Conversation"):
    st.session_state.pop("travel_agent", None)
    st.session_state.conversation_history = []
    st.rerun()

if "travel_agent" not in st.session_state:
    st.session_state.travel_agent = travel_agent

if "last_input" not in st.session_state:
    st.session_state.last_input = ""

if "current_context" not in st.session_state:
    st.session_state.current_context = ""
# Display conversation history
st.subheader("Conversation History")
for i, (role, message) in enumerate(st.session_state.conversation_history):
    if role == "user":
        st.write(f"👤 You: {message}")
    else:
        st.write(f"🧠 Agent: {message}")
 
if(st.session_state.current_context!=""):
    with st.spinner("Thinking..."):
        response = travel_agent.generate(st.session_state.current_context)
        # Add bot response to history
        st.session_state.conversation_history.append(("bot", response))
        st.session_state.current_context=""
        st.write(f"🧠 Agent: {response}")
        
        
# Form to handle Enter submission
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask me anything about your travel plans:")
    submitted = st.form_submit_button("Submit Answer")
    
    if submitted and user_input.strip():
        st.session_state.conversation_history.append(("user", user_input))
        history = st.session_state.conversation_history[-10:]  # get last 5 exchanges
        context = f"system: {system_prompt}\n"
        for role, message in history:
            if role == "user":
                context += f"User: {message}\n"
            else:
                context += f"Agent: {message}\n"
                
        st.session_state.current_context=context
        st.rerun()
