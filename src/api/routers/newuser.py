from pydantic import BaseModel
from fastapi import APIRouter
from src.database.crud import CrudHelper


router = APIRouter(prefix="/users", tags=["Users"])
crud = CrudHelper()

class NewUser(BaseModel):
    name : str
    email : str
    password : str

class NewUserResponse(BaseModel):
    message : str

@router.post("/", response_model=NewUserResponse)
async def new_user_api(body : NewUser):
    crud.new_user(name=body.name, email=body.email, password=body.password)
    return NewUserResponse(message="nuevo usuario creado")



