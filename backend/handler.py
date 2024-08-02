import logging
import time
from typing import Annotated

from annotated_types import Len
from faststream.rabbit import RabbitRouter
from pydantic import BaseModel, Field, PositiveInt

log = logging.getLogger(__name__)
router = RabbitRouter()  # prefix="prefix_"  >>  queue="prefix_que2"


class UserInfo(BaseModel):
    name: Annotated[str, Len(min_length=2, max_length=20)]
    user_id: PositiveInt = Field(examples=[1])


@router.subscriber("que1")
async def base_handler_1(user: UserInfo):
    log.info(user.name)
    log.info(user.user_id)


@router.subscriber("que2")
async def base_handler_2(msg: str):
    log.info(msg)


# ======================================================================================

# filter subscriber состоит из фильтра и дефолта
# фильтр принимает json, а остальное идет в дефолт
subscriber3 = router.subscriber("que3")


@subscriber3(filter=lambda msg: msg.content_type == "application/json")
@router.publisher("que1")  # can be used only with functions decorated by a @subscriber
# @broker.publisher("que2")  # broadcast
async def json_handler(name: str, user_id: int):
    log.info("%s, %s", name, user_id)
    time.sleep(2)
    return {"name": name, "user_id": user_id}


# Publisher object включает функции тестируемости
# используется совместно с @subscriber образуя pipeline
publisher1 = router.publisher("que1")  # raise Validation error: input UserInfo object


@publisher1
@subscriber3
async def default_handler_3(msg: str):
    log.info(msg)


# ======================================================================================

publisher2 = router.publisher("que2")
subscriber4 = router.subscriber("que4")


@publisher2
@subscriber4
async def default_handler_4(msg: str):
    log.info(msg)
    time.sleep(msg.count("."))
    return msg


"""from faststream import Depends
def simple_dependency():
    return 1
#with @subscriber and @publisher
#1
broker = RabbitBroker(dependencies=[Depends(simple_dependency)])
#2
@broker.subscriber("test", dependencies=[Depends(simple_dependency)])
def method(): ...
#3
@broker.subscriber("test")
def method(_ = Depends(simple_dependency)): ...

#OR
@apply_types
def method(a: int = Depends(simple_dependency)):
    return a
"""
