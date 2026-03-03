from src.deepagent.tools.toolkit import DockerSandboxToolKit
from typing import TypedDict, Annotated, Sequence, Literal, List
from ..tools.tools import write_todos, task_completed
from operator import add
from src import settings

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage

from langgraph.graph import add_messages, StateGraph, START, END
from langgraph.prebuilt import ToolNode


# TODO: Falta agregar loggers
from src.logging_conf import get_logger
logger = get_logger(module_name="deepagent", DIR="nose")


class Todo(TypedDict):
    content : str
    status : Literal["pending", "in_progress", "completed"] 


def create_my_deep_agent(llm : BaseChatModel, base_system_message : str):

    toolkit = DockerSandboxToolKit(image=settings.DOCKER_SANDBOX_IMAGE_NAME)
    tools_sandbox = toolkit.get_tools()
    tools = tools_sandbox + [write_todos, task_completed]

    llm_with_tools = llm.bind_tools(tools=tools)

    class State(TypedDict):
        messages : List[BaseMessage]
        todos : List[Todo]
        end : bool 
    
    tools_invoker = ToolNode(tools=tools, messages_key="messages")

    def ReAct_node(state : State) -> State:
        messages = state["messages"]
        todos = state["todos"]
        end = False

        ai_message = llm_with_tools.invoke(messages)

        for tool_call in ai_message.tool_calls:
            if tool_call['name'] == "write_todos":
                todo = tool_call["args"]
                todos.append(todo)
                system_message = base_system_message.format(todos=todos)
                messages[0] = system_message
            if tool_call['name'] == "task_completed":
                end = True

            
        messages.append(ai_message)
        return {"messages":messages, "todos":todos, "end":end}

                

    def should_end(state : State) -> Literal["tool_node_wrapper", END]: # type: ignore
        if state["end"]:
            return END
        return "tool_node_wrapper"


    def tool_node_wrapper(state : State) -> State:
        messages = state["messages"]

        tools_responses = tools_invoker.invoke(state)
        messages += tools_responses["messages"]
        return {"messages":messages}
    
    
    builder = StateGraph(State)

    builder.add_node("ReAct_node", ReAct_node)
    builder.add_node("tool_node_wrapper", tool_node_wrapper)

    builder.add_edge(START, "ReAct_node")
    builder.add_conditional_edges("ReAct_node", should_end)
    builder.add_edge("tool_node_wrapper", "ReAct_node")

    return builder.compile()




