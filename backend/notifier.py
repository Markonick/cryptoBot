from typing import List
from starlette.websockets import WebSocket

import asyncio
from aio_pika import connect, Message, IncomingMessage, ExchangeType


class Notifier:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.is_ready = False

    async def setup(self, queue_name: str):
        self.connection = await connect(
            "amqp://guest:guest@rabbitmq/",
            loop=asyncio.get_running_loop()
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

        # Declare an exchange
        exchange = await self.channel.declare_exchange(
            "ticker", ExchangeType.TOPIC
        )

        # Declaring queue
        queue = await self.channel.declare_queue(
            "ticker_queue", durable=True
        )

        await queue.bind(exchange, routing_key='ticker')
        await queue.consume(self.on_message, no_ack=True)
        print('after queue consume')
        self.is_ready = True

    async def push(self, msg: str):
        await self.channel.default_exchange.publish(
            Message(msg.encode("ascii")),
            routing_key='ticker',
        )

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def on_message(self, message: IncomingMessage):
        living_connections = []
        while len(self.connections) > 0:
            print(len(self.connections))
            websocket = self.connections.pop()
            await websocket.send_text(f"{message.body}")
            living_connections.append(websocket)
        self.connections = living_connections