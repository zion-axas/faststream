"""
Existing Fields: broker, context, logger, message
context=Context()
context.set_global("key", Any)
key: str=Context(default=None, cast=True)
lst: list[str]=Context(initial=list)
"""

from typing import Annotated

from faststream import Context, ContextRepo, Logger, apply_types
from faststream.rabbit import RabbitMessage, RabbitRouter
from faststream.rabbit.annotations import (
    # ContextRepo,
    # Logger,
    # NoCast,
    # RabbitMessage,
    # RabbitProducer,
    RabbitBroker,
)

router = RabbitRouter()
CorrelationId = Annotated[
    str, Context("message.correlation_id", default=None, cast=True)
]


# que5 catches after_startup 'Hello' message
@router.subscriber("que5")
async def handler_5(
    msg: str,
    correlation_id: CorrelationId,
    headers: str = Context("message.headers.user", default=""),
    context=Context(),  # the context itself, in which you can write your own fields
    broker=Context(),  # the current broker
    logger=Context(),  # the logger used for your broker (tags messages with message_id)
    message=Context(),  # the raw message (if you need access to it)
):
    # using context to store own object
    context.set_global("secret_str", "my-perfect-secret")  # set global

    if msg == "Hello":
        logger.warning("RAW:\n%s", message)
        await broker.publish(msg, queue="que6")
    logger.info(msg)


@router.subscriber("que6")
async def handler_6(
    msg: str,
    broker: RabbitBroker,  # the current broker
    context: ContextRepo,  # the context itself, in which you can write your own fields
    logger: Logger,  # the logger used for your broker (tags messages with message_id)
    message: RabbitMessage,  # the raw message (if you need access to it)
    secret_str: str = Context(),
):
    logger.info(msg)

    assert secret_str == "my-perfect-secret"

    context.reset_global("secret_str")  # del global

    # To set a local context (available only within the message processing scope),
    # use the context manager scope
    with context.scope("another_secret", "333"):
        call()


# По умолчанию поля контекста НЕ ПРИВОДЯТСЯ к типу, указанному в их аннотации:
# secret: int = Context() - str не приведется к int
# cast=True - привести к типу


@apply_types
def call(
    logger: Logger,
    another_secret: int = Context(cast=True, default=None),  # OR new name:
    new_name_another_secret: str = Context("another_secret"),
    collector: list[str] = Context(initial=list),  # without previous set_global call
):
    assert another_secret == 333

    logger.warning("call() - %s", new_name_another_secret)

    collector.append(another_secret)
