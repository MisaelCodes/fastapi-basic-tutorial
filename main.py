from enum import Enum
from typing import Annotated, Literal

from fastapi import FastAPI, Body, Query
from pydantic import BaseModel

app = FastAPI()


class Notification(str, Enum):
    email = "email"
    whatsapp = "whatsapp"
    text = "text"


class FilterParams(BaseModel):
    model_config = {"extra": "ignore"}
    notify: Notification
    sync: Literal["now", "later", "never"] = "now"


class Action(BaseModel):
    laucher: str
    args: str


class Task(BaseModel):
    name: str
    description: str
    time: str  # this should be datetime
    action: Action


@app.get("/")
async def root(q: Annotated[str | None, "This is metadata"] = None):
    res = {"message": "Hello World"}
    if q:
        res["q"] = q
    return res


@app.post("/v1/taskLists/{id}/tasks/")
async def create_list_task(
    id: int, q: Annotated[FilterParams, Query()], task: Annotated[Task, Body()]
):
    return {"id": id, "q": q, "task": task}
