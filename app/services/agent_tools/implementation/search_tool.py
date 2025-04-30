from pydantic import BaseModel
from langchain.agents import Tool
from langchain.tools import StructuredTool
from langchain_community.tools import DuckDuckGoSearchRun
from app.services.agent_tools.interface.tool_interface import AgentToolInterface
from app.utilities import shubham_logger
from app.utilities.constants import Constants


logger = shubham_logger.ShubhamLogger(shubham_logger.get_logger(__name__),{"travel-agent":"v1"})



class SearchInput(BaseModel):
    """
    This it the tool input structure
    Author: Shubham Sharma

    Args:
        BaseModel (_type_): _description_
    """
    query: str


class SearchTool(AgentToolInterface):
    """
    This tool is used for searching the web for the given query.
    The agent will decide when to use this tool based on the provided tools discription which is fetched from 
    constants.yaml file.
    
    author: Shubham Sharma
    Args:
        AgentToolInterface (_type_):
    """
    
    def __init__(self) -> None:
        self.name = "DuckDuckGoSearch"
        self.search = DuckDuckGoSearchRun()
        self.description = Constants.fetch_constant("tools_descriptions")["search_tool"]
        
    def search_duckduckgo(self,query):
        """
        This function is called by the agent to perfrom a web seach.

        Args:
            query (_type_): _description_

        Raises:
            exe: _description_

        Returns:
            _type_: _description_
        """
        logger.info(
            f"!!!! Searching for {query} for web search!!!!!"
        )
        try:
            logger.info("Started using duckduckgo tool....")
            results =  self.search.run(query, verbose=True)

            # Return the results as a string
            logger.info(f"Search Results for query={query}\n {results}")
            return results
        except Exception as exe:
            logger.error(f"error while using search duckduckgo tool: {exe}")
            raise exe

    def get_tool(self) -> Tool:
        """
        this method returns the Tool object with it's discription and main function.
        Here is the counter part for openai functions.

        Returns:
            Tool: _description_
        """
        return StructuredTool.from_function(
            name=self.name,
            description=self.description,
            func=self.search_duckduckgo,
            args_schema=SearchInput,
        )
        
