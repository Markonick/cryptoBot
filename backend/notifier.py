from typing import List
from starlette.websockets import WebSocket
import json
import asyncio
from aio_pika import connect, Message, IncomingMessage, ExchangeType
from entities import Tick
from dataclasses import fields

class Notifier:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.is_ready = False

    async def setup(self, symbols: List):
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
        for i, symbol in enumerate(symbols):
            queue = await self.channel.declare_queue(
                f"{symbol}", durable=True
            )

            await queue.bind(exchange, routing_key=f"{symbol}")
            await queue.consume(self.on_message, no_ack=True)
            print(f"after {symbol} queue consume")
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
            msg = json.loads((message.body).decode('UTF-8'))
            
            attributes = [field.name for field in fields(Tick)]
            tick_dict = {attributes[i]: v for i, v in enumerate(msg.values())}
            # tick = Tick(**tick_dict)
            print(tick_dict)
            # print(tick)
            await websocket.send_json(tick_dict)
            living_connections.append(websocket)
            print(len(living_connections))
        self.connections = living_connections