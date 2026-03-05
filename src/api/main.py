from fastapi import FastAPI
from src.api.routers import newchats, newuser, runchat, run_educhat

app = FastAPI(title="Chat edubot")

app.include_router(newuser.router)
app.include_router(newchats.router)
app.include_router(runchat.router)
app.include_router(run_educhat.router)

"""
uvicorn src.api.main:app --host 0.0.0.0 --port 8000

"""