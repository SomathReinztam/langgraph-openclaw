from typing import TypedDict, Annotated, List, Literal
from operator import add

from langchain_core.messages import BaseMessage, AIMessage

from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import add_messages


class Todo(TypedDict):
    content : str
    status : Literal["pending", "in_progress", "completed"]


def create_dummie_agent() -> CompiledStateGraph:

    class State(TypedDict):
        messages : Annotated[List[BaseMessage], add_messages]
        todos : List[Todo]

    def dommie_react_node(state : State) -> State:
        ai_message = AIMessage(content=".")
        ai_message.tool_calls = [{}]
        return ai_message
    
    