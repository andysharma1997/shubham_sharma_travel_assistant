from typing import List
from langchain import hub
from langchain.agents import Tool
from langchain.agents import AgentExecutor, create_react_agent, create_structured_chat_agent
from langchain.chat_models import init_chat_model
from langchain.memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from tenacity import retry,stop_after_attempt
from app.services.agent_tools.implementation.search_tool import SearchTool
from app.utilities import shubham_logger

logger = shubham_logger.ShubhamLogger(shubham_logger.get_logger(__name__),{"travel-agent":"v1"})


class SmartTravelAgent:
    """
    This is the agent that will have the conversation with the user and will use the search tool(can be extended), to give response.
    The Agent also has a conversation memory to keep track of the context.
    
    Author: Shubham Sharma
    """
    def __init__(self,tools: List[Tool]):
        llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        self.memory = ChatMessageHistory(session_id="test_session") # session_id isn't really used here because we are using a simple in memory ChatMessageHistory
        prompt = hub.pull("hwchase17/structured-chat-agent")
        # print("prompt xx  \n",prompt.messages[0].prompt.template)
        
        # Add our custom instructions
        prompt.messages[0].prompt.template += """

        IMPORTANT: When using the DuckDuckGoSearch tool, ALWAYS format your action_input with a "query" parameter, like this:
        ```
        {{
        "action": "DuckDuckGoSearch",
        "action_input": {{
            "query": "Your search query here"
        }}
        }}
        ```
        DO NOT use "title" or other parameters when calling the search tool.
        """
        agent = create_structured_chat_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)

        self.agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: self.memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        
    @retry(stop=stop_after_attempt(2))
    def generate(self,query: str):
        """
        This method will be called from the UI for each user query.

        Author: Shubham Sharma

        Args:
            query (str): _description_
        """
        try:
            response = self.agent_with_chat_history.invoke(
                {"input": query},
                config={"configurable": {"session_id": "<foo>"}}
            )
            
            return response["output"]
        except Exception as e:
            logger.error(f"Error in generate: {str(e)}")
            return f"I encountered an error while processing your request. Please try rephrasing or ask another question."


