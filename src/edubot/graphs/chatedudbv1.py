from typing import TypedDict, Annotated, List, Literal
from sqlalchemy.engine import Engine
from src.edubot.tools.toolkit import PostgresToolKit
from src.utils.logging_config import get_logger

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage

from langgraph.graph import add_messages, StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.state import CompiledStateGraph

logger = get_logger(module_name="chatv1", DIR="edubot")

def create_educhat(llm : BaseChatModel, engine : Engine) -> CompiledStateGraph:

    pg_toolkit = PostgresToolKit(engine=engine)
    pg_tools = pg_toolkit.get_tools()

    llm_with_tools = llm.bind_tools(tools=pg_tools)

    class State(TypedDict):
        messages : Annotated[List[BaseMessage], add_messages]

        input_tokens : int
        output_tokens : int
        api_calls : int
    

    
    tool_invoker = ToolNode(tools=pg_tools, messages_key="messages")

    def ReAct_node(state : State) -> State:
        logger.info("xxx"*5 + " ReAct_node " + "xxx"*5)
        messages = state["messages"]

        input_tokens = state.get("input_tokens", 0)
        output_tokens = state.get("output_tokens", 0)
        api_calls = state.get("api_calls", 0)


        ai_message = llm_with_tools.invoke(messages)
        logger.info(f"\n {ai_message.pretty_repr()} \n")

        #TODO: no se esta contando bien los tokens y las calls
        input_tokens += ai_message.usage_metadata.get("input_tokens", 0)
        output_tokens += ai_message.usage_metadata.get("output_tokens", 0)
        api_calls += 1

        logger.info(f"input_tokens: {input_tokens}--output_tokens: {output_tokens}--api_calls: {api_calls}")
        return {"messages":ai_message, "input_tokens":input_tokens, "output_tokens":output_tokens, "api_calls":api_calls}
    

    def tool_node_wrapper(state : State) -> State:
        logger.info("xxx"*5 + " ReAct_node " + "xxx"*5)
        tool_messages = tool_invoker.invoke(state)

        for message in tool_messages["messages"]:
            logger.info(f"\n {message.pretty_repr()}")

        return tool_messages
    

    def should_end(state : State) -> Literal["tool_node_wrapper", END]: # type: ignore
        logger.info("---"*5 + " ReAct_node ")
        last_ai_message = state["messages"][-1]
        if last_ai_message.tool_calls:
            logger.info("tool_node_wrapper")
            return "tool_node_wrapper"
        logger.info("END")
        return END
    

    builder = StateGraph(State)

    builder.add_node("ReAct_node", ReAct_node)
    builder.add_node("tool_node_wrapper", tool_node_wrapper)

    builder.add_edge(START, "ReAct_node")
    builder.add_conditional_edges("ReAct_node", should_end)
    builder.add_edge("tool_node_wrapper", "ReAct_node")

    return builder.compile()





if __name__=="__main__":
    from langchain_google_genai import ChatGoogleGenerativeAI
    from sqlalchemy import URL, create_engine
    from langchain_core.messages import SystemMessage, HumanMessage
    from src.edubot.prompts.educhatv1 import SYSTEM_PROMPT_4
    from src.edubot.prompts.agent import DB_SKILL_1
    from src.utils.logging_config import setup_base_logging
    from src.utils import settings

    setup_base_logging()

    db_user = settings.DB_USER
    db_pass = settings.DB_PASS
    db_host = settings.DB_HOST
    db_port = settings.DB_PORT
    db_name = settings.DB_NAME

    conn_url = URL.create(
        drivername="postgresql+psycopg2",
        username=db_user,
        password=db_pass,
        host=db_host,
        port=db_port,
        database=db_name
    )

    engine = create_engine(conn_url)

    #model = "gemini-2.0-flash"
    model = "gemini-3.1-flash-image-preview"
    llm = ChatGoogleGenerativeAI(model=model, temperature=0.5, google_api_key=settings.GOOGLE_API_KEY)

    chat_agent = create_educhat(llm=llm, engine=engine)

    messages = [
            SystemMessage(
                content=SYSTEM_PROMPT_4.format(db_skill=DB_SKILL_1)
            )
        ]

    while True:
        human_message = input()
        print("\n"*2)
        if human_message in ["exit"]:
            break
        human_message = HumanMessage(content=human_message)
        messages.append(human_message)
        logger.debug(f"{human_message.pretty_repr()}")

        agent_response = chat_agent.invoke({"messages":messages}, config={"recursion_limit": 50}) 
        messages.append(agent_response["messages"])
        logger.info("\n"*10)




"""
python3 -m src.edubot.graphs.chatedudbv1

"""