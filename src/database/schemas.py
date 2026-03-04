from pydantic import BaseModel
from typing import Literal, Dict, Any, Union, List, TypedDict


# ------------------------
# ------------------------


class DatabaseError(Exception):
    """Excepción base para errores de base de datos"""
    pass


class UserNotFoundError(DatabaseError):
    """Excepción cuando no se encuentra un usuario"""
    pass


class ChatNotFoundError(DatabaseError):
    """Excepción cuando no se encuentra un chat"""
    pass


# ------------------------
# ------------------------


class ToolCalls(TypedDict):
    name : str
    args : Dict[str, Any]
    id : str
    type : str


class UsageMetadata(TypedDict):
    input_tokens: int
    output_tokens: int
    total_tokens: int
    input_token_details: Dict[str, Any]


class AiResponse(TypedDict):
    content : Any
    tool_calls : ToolCalls
    usage_metadata : UsageMetadata


class ToolResponse(TypedDict):
    content : Any
    tool_call_id : str
    name : str


EduchatResponseItem = Union[AiResponse, ToolResponse]


class RunEduChatResponse(TypedDict):
    educhat_response : List[EduchatResponseItem]
    



# ------------------------
# ------------------------

class ChatModelProvider(BaseModel):
    client : Literal["google", "groq", "deepseek"]
    model : str
    temperature : float
    