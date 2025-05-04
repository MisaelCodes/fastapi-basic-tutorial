from enum import Enum
from typing import Annotated, Literal

from fastapi import Body, FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


# query parameters
class Notification(str, Enum):
    email = "email"
    whatsapp = "whatsapp"
    text = "text"


class FilterParams(BaseModel):
    model_config = {"extra": "ignore"}
    notify: Notification = Field(title="Way to notify that a task has been created", description="There are three different options")
    sync: Literal["now", "later", "never"] = "now"


# Body with nested models
class Action(BaseModel):
    laucher: str=Field(max_length=8)
    args: str


class Task(BaseModel):
    name: str = Field(
        title="The name of the given task",
        description="Tells what the task is, in a compacted form",
    )
    description: str|None = Field(
        default=None,
        title="The description of the task",
        description="tells the details of a given task or the purpose of it",
    )
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
