from langgraph.graph.state import CompiledStateGraph
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.utils import settings
from src.database import models
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage, ToolCall
from src.database.schemas import ChatModelProvider, RunEduChatResponse

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_deepseek import ChatDeepSeek

from src.edubot.graphs.chatedudbv1 import create_educhat


# TODO: faltan logs
from src.utils.logging_config import get_logger
logger = get_logger(module_name="run_educhat", DIR="database")


def run_educhat(user_id : int, chat_id : int, human_message : str, system_prompt : str, educhat : CompiledStateGraph) -> RunEduChatResponse:

    # conexion a la base de datos de la app
    conn_string = f"postgresql+psycopg2://{settings.APP_DB_USER}:{settings.APP_DB_PASS}@{settings.APP_DB_HOST}:{settings.APP_DB_PORT}/{settings.APP_DB_NAME}"
    engine = create_engine(conn_string)
    Session = sessionmaker(bind=engine)
    session = Session()

    # guardamos el mensaje del usuario en la db
    messages_model_record = models.MessageModel(
    user_id=user_id,
    chat_id=chat_id,
    role="Human",
    message={"content" : human_message}
    )
    session.add(messages_model_record)
    session.flush()

    # memoria del agente
    messages = [
        SystemMessage(content=system_prompt)
    ]

    # recuperamos el historial de la conversacion
    message_history = session.query(models.MessageModel).filter_by(user_id=user_id, chat_id=chat_id).order_by(models.MessageModel.date.asc()).all()
    
    for msg in message_history:
        if msg.role == "Human":
            messages.append(HumanMessage(content=msg.message['content']))
        elif msg.role == "Ai":
            data = msg.message

            content = data['content']
            tool_calls = data['tool_calls']
            usage_metadata = data['usage_metadata']

            langchain_tool_calls = []
            if len(tool_calls) > 0:
                langchain_tool_calls = [
                    ToolCall(
                        name=call['name'],
                        args=call['args'],
                        id=call['id'],
                        type=call['type']
                    ) for call in tool_calls
                ]
            
            messages.append(
                AIMessage(
                    content=content,
                    tool_calls=langchain_tool_calls,
                    usage_metadata = usage_metadata
                )
            )
        
        elif msg.role == "Tool":
            data = msg.message

            messages.append(
                ToolMessage(
                    content=data['content'],
                    tool_call_id=data['tool_call_id'],
                    name=data['name']
                )
            )


    # Haciendo inferencia
    agent_response = educhat.invoke({"messages":messages})
    messages = agent_response["messages"]

    # respuesta de `run_educhat`
    api_response = []

    N = len(messages)-1
    for i in range(N):
        msg = messages[N-i]
        if isinstance(msg, HumanMessage):
            break

        if isinstance(msg, AIMessage):
            content = msg.content
            tool_calls = [
                {
                    'name':call['name'],
                    'args':call['args'],
                    'id':call['id'],
                    'type':call['type']
                }
                for call in msg.tool_calls
            ]
            usage_metadata = msg.usage_metadata
            
            message_data = {'content':content, 'tool_calls':tool_calls, 'usage_metadata':usage_metadata}
            messages_model_record = models.MessageModel(
                user_id=user_id,
                chat_id=chat_id,
                role="Ai",
                message=message_data
            )

            session.add(messages_model_record)
            session.flush()
            api_response.append(message_data)

        if isinstance(msg, ToolMessage):
            content = msg.content
            tool_call_id = msg.tool_call_id
            name = msg.name

            message_data = {'content':content, 'tool_call_id':tool_call_id, 'name':name}
            messages_model_record = models.MessageModel(
                user_id=user_id,
                chat_id=chat_id,
                role="Tool",
                message=message_data
            )

            session.add(messages_model_record)
            session.flush()
            api_response.append(message_data)


    session.commit()
    session.close()
    api_response = list(reversed(api_response))  

    return {'educhat_response':api_response}





def config_educhat(user_id : int, chat_id : int) -> CompiledStateGraph:

    # conexion a la base de datos de la app
    conn_string_app = f"postgresql+psycopg2://{settings.APP_DB_USER}:{settings.APP_DB_PASS}@{settings.APP_DB_HOST}:{settings.APP_DB_PORT}/{settings.APP_DB_NAME}"
    engine = create_engine(conn_string_app)
    Session = sessionmaker(bind=engine)
    session = Session()

    # .first(), .one() o .one_or_none():
    provider = session.query(models.ChatModel).filter_by(user_id=user_id, chat_id=chat_id).first()

    # Validando
    provider_conf = ChatModelProvider(**provider.chat_model_provider)

    # creando engine para la base de datos edubot
    conn_string_edubot = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    engine_edubot = create_engine(conn_string_edubot)


    if provider_conf.client == "google":
        llm = ChatGoogleGenerativeAI(model=provider_conf.model, temperature=provider_conf.temperature, google_api_key=settings.GOOGLE_API_KEY)
        educhat = create_educhat(llm=llm, engine=engine_edubot)
        return educhat
    elif provider_conf.client == "groq":
        llm = ChatGroq(model=provider_conf.model, temperature=provider_conf.temperature, api_key=settings.GROQ_API_KEY)
        educhat = create_educhat(llm=llm, engine=engine_edubot)
        return educhat
    elif provider_conf.client == "deepseek":
        llm = ChatDeepSeek(model=provider_conf.model, temperature=provider_conf.temperature, api_key=settings.DEEPSEEK_API_KEY)
        educhat = create_educhat(llm=llm, engine=engine_edubot)
        return educhat
    





"""
python3 -m src.database.run_chat

"""
