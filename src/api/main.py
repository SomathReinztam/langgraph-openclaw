from fastapi import FastAPI
from src.api.routers import newchats, newuser, runchat

app = FastAPI(title="Chat edubot")

app.include_router(newuser.router)
app.include_router(newchats.router)
app.include_router(runchat.router)


