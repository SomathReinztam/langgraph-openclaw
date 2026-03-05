from pydantic import BaseModel
from typing import List, Dict, Any, Union
from fastapi import APIRouter
from src.database.run_chat import run_educhat, config_educhat
from src.edubot.prompts.agent import DB_SKILL_1
from src.edubot.prompts.educhatv1 import SYSTEM_PROMPT_4

router = APIRouter(prefix="/runeduchat", tags=["Runeduchat"])

class RundEduChat(BaseModel):
    user_id : int
    chat_id : int
    human_message : str


# -----------------------
# -----------------------



# class ToolCalls(BaseModel):
#     name : str
#     args : Dict[str, Any]
#     id : str
#     type : str


# class UsageMetadata(BaseModel):
#     input_tokens: int
#     output_tokens: int
#     total_tokens: int
#     input_token_details: Dict[str, Any] | None = None
#     output_token_details : Dict[str, Any] | None = None


# class AiResponse(BaseModel):
#     content : Any
#     tool_calls : List[ToolCalls]
#     usage_metadata : UsageMetadata
#     type : str


# class ToolResponse(BaseModel):
#     content : Any
#     tool_call_id : str
#     name : str
#     type : str


# EduchatResponseItem = Union[AiResponse, ToolResponse]


class RunEduChatResponse(BaseModel):
    educhat_response : List[Dict[str, Any]]



# -----------------------
# -----------------------


@router.post("/", response_model=RunEduChatResponse)
async def run_educhat_api(body : RundEduChat):
    educhat = config_educhat(user_id=body.user_id, chat_id=body.chat_id)
    print("A"*80)
    prompt = SYSTEM_PROMPT_4.format(db_skill=DB_SKILL_1)
    agent_response = run_educhat(user_id=body.user_id, chat_id=body.chat_id, human_message=body.human_message, system_prompt=prompt, educhat=educhat)
    print("B"*80)
    return agent_response




