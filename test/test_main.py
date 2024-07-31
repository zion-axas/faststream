import pytest
from faststream.rabbit import TestRabbitBroker

from backend.main import broker, json_handler
from config import settings


@pytest.mark.asyncio
async def test_handler():
    await json_handler("John", settings.TEST_ID)


# using TestClient
@pytest.mark.asyncio
async def test_handle():
    async with TestRabbitBroker(broker) as br:  # with_real=True  - Real Broker Testing
        await br.publish({"name": "John", "user_id": 2}, queue="test3")
        await br.publish("message", queue="test3")
        await json_handler.wait_call(timeout=3)  # timeout for real testing
        
        # mock object to validate your input
        json_handler.mock.assert_called_once_with({"name": "John", "user_id": 2})

    assert json_handler.mock is None  # mock objects cleared when the context exits
