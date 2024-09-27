from fastapi import FastAPI
from pydantic import BaseModel

from src.auth.router import router

app = FastAPI()


class Look(BaseModel):
    name: str
    description: str | None


@app.get("/looks/")
async def create_look():
    look = Look(name="My First Look", description="A simple look for beginners")
    return look


app.include_router(router=router)


