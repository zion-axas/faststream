from faststream import Context
from faststream.rabbit import ExchangeType, RabbitExchange, RabbitQueue, RabbitRouter

from backend.main import broker

router = RabbitRouter()

exch = RabbitExchange("exchange", type=ExchangeType.FANOUT)
queue_1 = RabbitQueue("test-q-1")  # durable
queue_2 = RabbitQueue("test-q-2")


@router.subscriber(queue_1, exch)  # no_ack
async def handler_1(logger=Context()):
    logger.info("exch_handler_1")


@router.subscriber(queue_1, exch)
async def handler_2(logger=Context()):
    logger.info("exch_handler_2")


@router.subscriber(queue_1, exch)
async def handler_3(logger=Context()):
    logger.info("exch_handler_3")


async def send_messages_fanout():
    await broker.publish(exchange=exch)  # handlers: 1, 3 # persist
    await broker.publish(exchange=exch)  # handlers: 2, 3
    await broker.publish(exchange=exch)  # handlers: 1, 3
    await broker.publish(exchange=exch)  # handlers: 2, 3


# When sending messages to Fanout exchange ^^^^, it makes no sense to specify the
# arguments queue or routing_key, because they will be ignored.


exch = RabbitExchange("exchange", type=ExchangeType.TOPIC)
queue_1 = RabbitQueue("test-queue-1", routing_key="*.info")
queue_2 = RabbitQueue("test-queue-2", routing_key="*.debug")


async def send_messages_topic():
    await broker.publish(routing_key="logs.info", exchange=exch)  # handlers: 1
    await broker.publish(routing_key="logs.info", exchange=exch)  # handlers: 2
    await broker.publish(routing_key="logs.info", exchange=exch)  # handlers: 1
    await broker.publish(routing_key="logs.debug", exchange=exch)  # handlers: 3
