# https://faststream.airt.ai/latest/rabbit/publishing/

# python backend/pub.py :: [str], [..], [int], json, q

"""4 варианта отравки сообщений

broker.publish(msg, queue)
@broker.publisher(queue)                                            # AsyncAPI
publisher = broker.publisher(queue) => @publisher                   # AsyncAPI; testing
publisher = broker.publisher(queue) => publisher.publish(msg)       # AsyncAPI; testing

2 и 3 отправляют одно сообщение, но возможна рассылка
4 способ позволяет отправить несколько сообщений из одной функции
"""

import asyncio
import time

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from config import settings

broker = RabbitBroker(settings.BROKER)
app = FastStream(broker)


@app.after_startup
async def test():
    msg = ""
    while msg != "q":
        msg = input("input: ")
        if msg == "json":
            msg = {"name": "IVAN", "user_id": "13"}
            await broker.publish(msg, queue="que3")
            continue
        if msg.isnumeric():
            for i in range(int(msg)):
                await broker.publish(f"test_message {i}", queue="que4")
                time.sleep(0.2)
        await broker.publish(msg, queue="que4")


async def main():
    await app.run()  # blocking method


if __name__ == "__main__":
    asyncio.run(main())
