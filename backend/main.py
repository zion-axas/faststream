from faststream import FastStream
from faststream.rabbit import RabbitBroker

from backend.handler import router
from config import configure_logging

configure_logging()


broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
# apply_types=False  - decorator disable Pydantic validation, Depends, Context
# validate=False  - disable validation

broker.include_router(router=router)

app = FastStream(broker)


@app.after_startup
async def test():
    await broker.publish("Hello", queue="que4")
