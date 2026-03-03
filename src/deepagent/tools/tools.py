from pydantic import BaseModel, Field
from typing import Literal, List
from langchain_core.tools import StructuredTool

class Todo(BaseModel):
    content : str = Field(description=".")
    status : Literal["pending", "in_progress", "completed"] = Field(description=".")



def _write_todos(todo : Todo) -> str:
    return f"Lista de pendientes (todos) actualizada con: {todo}"


write_todos = StructuredTool.from_function(
    name="write_todos",
    description=".",
    func=_write_todos,
    args_schema=Todo
)




def _task_completed() -> str:
    return ""


task_completed = StructuredTool(
    name="task_completed",
    description=".",
    func=_task_completed
)
