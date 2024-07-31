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


@broker.subscriber("que1")
async def base_handler(user: UserInfo):
    log.info(user.name)
    log.info(user.user_id)


@broker.subscriber("que2")
async def base_handler_(msg: str):
    log.info(msg)


# ======================================================================================

# filter subscriber состоит из фильтра и дефолта
# фильтр принимает json, а остальное идет в дефолт
subscriber3 = broker.subscriber("que3")


@subscriber3(filter=lambda msg: msg.content_type == "application/json")
@broker.publisher("que1")  # can be used only with functions decorated by a @subscriber
# @broker.publisher("que2")  # broadcast
async def json_handler(name: str, user_id: int):
    log.info("%s, %s", name, user_id)
    return {"name": name, "user_id": user_id}


# Publisher object включает функции тестируемости
# используется совместно с @subscriber образуя pipeline
publisher1 = broker.publisher("que1")  # raise Validation error: input UserInfo object


@publisher1
@subscriber3
async def default_handler(msg: str):
    log.info(msg)


# ======================================================================================

publisher2 = broker.publisher("que2")
subscriber4 = broker.subscriber("que4")


@publisher2
@subscriber4
async def default_handler_(msg: str):
    log.info(msg)


@app.after_startup
async def test():
    await broker.publish("Hello", queue="que3")
