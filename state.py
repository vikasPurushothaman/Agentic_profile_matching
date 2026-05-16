from typing import Annotated, TypedDict, List, Dict, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
    job_description: str
    
    requirements: Dict[str, Any]
    
    shortlist: List[Dict[str, Any]]
    
    reports: Dict[str, str]
