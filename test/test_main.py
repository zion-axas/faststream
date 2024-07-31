import pytest
from faststream.rabbit import TestRabbitBroker
from pydantic import ValidationError

from backend.handler import json_handler, publisher2
from backend.main import broker
from config import settings


@pytest.mark.asyncio
async def test_json_handler():
    await json_handler("John", settings.TEST_ID)


# using TestClient
@pytest.mark.asyncio
async def test_handle_1():
    async with TestRabbitBroker(broker) as br:  # with_real=True  - Real Broker Testing
        await br.publish({"name": "John", "user_id": 2}, queue="que3")
        with pytest.raises(ValidationError):
            await br.publish("message", queue="que3")
        await json_handler.wait_call(timeout=3)  # timeout for real testing

        # mock object to validate your input
        json_handler.mock.assert_called_once_with({"name": "John", "user_id": 2})

    assert json_handler.mock is None  # mock objects cleared when the context exits


@pytest.mark.asyncio
async def test_handle_2():
    async with TestRabbitBroker(broker) as br:
        await br.publish("Hi!", queue="que4")
        # to check the outgoing message body:
        publisher2.mock.assert_called_once_with("Hi!")
