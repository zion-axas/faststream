import logging
from typing import Annotated

from annotated_types import Len
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from pydantic import BaseModel, Field, PositiveInt

from config import configure_logging

configure_logging()
log = logging.getLogger(__name__)

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
# apply_types=False  - disable Pydantic validation, Depends, Context
# validate=False  - disable validation

app = FastStream(broker)


class UserInfo(BaseModel):
    name: Annotated[str, Len(min_length=2, max_length=20)]
    user_id: PositiveInt = Field(examples=[1])


@broker.subscriber("test1")
@broker.subscriber("test2")
async def base_handler(user: UserInfo):
    log.info(user.name)
    log.info(user.user_id)


# filter subscriber состоит из фильтра и дефолта
# фильтр принимает json, а остальное идет в дефолт
subscriber = broker.subscriber("test3")


@subscriber(filter=lambda msg: msg.content_type == "application/json")
@broker.publisher("test1")  # can be used only with functions decorated by a @subscriber
# @broker.publisher("test2")  # broadcast
async def json_handler(name: str, user_id: int):
    log.info("%s, %s", name, user_id)
    return {"name": name, "user_id": user_id}


@subscriber
async def default_handler(msg: str):
    log.info(msg)


@app.after_startup
async def test():
    await broker.publish("Hello", queue="test3")
