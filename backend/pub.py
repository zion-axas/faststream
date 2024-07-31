import asyncio
# from time import sleep

from faststream import FastStream
from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")
app = FastStream(broker)


@app.after_startup
async def test():
    # tm = 210
    msg = ""
    while msg != "q":
        # print(tm)
        # msg = "tsst"
        msg = input("input: ")
        if msg == "json":
            msg = {"name": "IVAN", "user_id": "13"}
        await broker.publish(msg, queue="test3")
        # sleep(tm)
        # tm += 10


async def main():
    await app.run()  # blocking method


if __name__ == "__main__":
    asyncio.run(main())
