from pydantic import BaseModel
from fastapi import APIRouter
from src.database.crud import CrudHelper
from typing import TypedDict, Literal

router = APIRouter(prefix="/chats", tags=["Chats"])
crud = CrudHelper()


class ChatModelProvider(TypedDict):
    client : Literal["google", "groq", "deepseek"]
    model : str
    temperature : float



class NewChat(BaseModel):
    user_id : int
    chat_model_provider : ChatModelProvider

class NewChatResponse(BaseModel):
    message : str


@router.post("/", response_model=NewChatResponse)
async def new_chat_api(body : NewChat):
    crud.new_chat(user_id=body.user_id, chat_model_provider=body.chat_model_provider)
    return NewChatResponse(message="nuevo chat")


