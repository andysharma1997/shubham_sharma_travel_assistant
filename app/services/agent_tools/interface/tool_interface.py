from abc import abstractmethod, ABC
from app.utilities.singleton_factory import Singleton
from langchain.agents import Tool



class AgentToolInterface(metaclass=Singleton):
    
    @abstractmethod
    def get_tool(self) -> Tool:
        pass