from faststream import FastStream
from faststream.rabbit import RabbitBroker

from backend.handler import router as router_handler
from backend.context import router as router_context
from config import configure_logging

configure_logging()


broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
# apply_types=False  - decorator disable Pydantic validation, Depends, Context
# validate=False  - disable validation

broker.include_router(router=router_handler)
broker.include_router(router=router_context)

app = FastStream(broker)


@app.after_startup
async def test():
    await broker.publish("Hello", queue="que5")
