import logging

from faststream import ContextRepo, FastStream
from faststream.rabbit import RabbitBroker

from backend.context import router as router_context
from backend.handler import router as router_handler
from config import Settings, configure_logging, settings

configure_logging()


broker = RabbitBroker(settings.BROKER, log_level=logging.DEBUG)
# apply_types=False  - decorator disable Pydantic validation, Depends, Context
# validate=False  - disable validation

broker.include_router(router=router_handler)
broker.include_router(router=router_context)

app = FastStream(broker)


# faststream run backend.main:app --env .env.test
# the env field will be passed to the setup function from the args with the command line
# Command line args are available in all @app.on_startup hooks.
# To use them in other parts of the application, put them in the ContextRepo
@app.on_startup
async def setup(context: ContextRepo, env: str = ".env"):  # env from --env
    settings = Settings(_env_file=env)
    context.set_global("settings", settings)
    # await broker.connect(settings.BROKER)  # init broker if: broker = RabbitBroker()


@app.after_startup
async def test():
    await broker.publish("Hello", queue="que5")


# hooks:
# @app.on_startup           called BEFORE the broker is launched
# @app.after_startup        AFTER initializing the broker
# @app.on_shutdown          called BEFORE the broker is stopped
# @app.after_shutdown       triggered AFTER stopping the broker
# OR
# instead @app.on_startup & @app.after_shutdown
"""
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(context: ContextRepo, env: str = ".env"):
    # BEFORE the broker is launched
    settings = Settings(_env_file=env)
    context.set_global("settings", settings)
    
    yield
    # AFTER stopping the broker
"""
