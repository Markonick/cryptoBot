import typing, time, json, os, asyncio
from abc import ABC, abstractmethod
from typing import Optional, NewType
from fastapi import FastAPI, WebSocket, Depends, status
from starlette.websockets import WebSocketDisconnect
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.middleware.cors import CORSMiddleware
import pika
import asyncpg

from repositories import RabbitMqTickerRepository
from services import TickerService
from notifier import Notifier


SCHEMA = os.environ.get("SCHEMA")
EXCHANGE = os.environ.get("RABBITMQ_EXCHANGE")
HOST = os.environ.get("RABBITMQ_HOST")
PORT = os.environ.get("RABBITMQ_PORT")
QUEUE = os.environ.get("RABBITMQ_QUEUE")
RABBITMQ_KLINES_TOPIC = os.environ.get("RABBITMQ_KLINES_TOPIC")
API_BASE_URL = os.environ.get("API_BASE_URL")

app = FastAPI()
notifier = Notifier()
router = InferringRouter()
app.add_middleware(CORSMiddleware, allow_origins=["*"])
config={'exchange': EXCHANGE, 'host': HOST, 'port': PORT}

class ISubscriber(ABC):       
    @abstractmethod 
    async def consume(self, data: dict) -> None:
        pass

# class RabbitmqSubscriber(ISubscriber):
#     """
#     RabbitMQ implementation of IPublisher 
#     """
#     def __init__(self, queueName, bindingKey, config):
#       self._queueName = queueName
#       self._bindingKey = bindingKey
#       self._config = config
#       print(self._config)
  
#     # def __del__(self):
#     #     self._connection.close()

#     def _create_connection(self):
#         parameters = pika.ConnectionParameters(host=self._config['host'], port = self._config['port'])
#         return pika.BlockingConnection(parameters)

#     def _on_message_callback(self, channel, method, properties, body):
#         binding_key = method.routing_key
#         # print(f"received new message for - {binding_key}")
 
#         print(" [x] Received %r" % body)
#         time.sleep(body.count(b'.'))
#         print(" [x] Done")

#         print('==========JSON.LOADS: =============')
#         json_loads_msg = json.loads(body)
#         print(json_loads_msg)
#         self._msg = json_loads_msg
#         print("delivery_tag")
#         print("delivery_tag")
#         print("delivery_tag")
#         print(method.delivery_tag)
#         channel.basic_ack(delivery_tag = method.delivery_tag)

#     def consume(self):
#         connection = self._create_connection()
#         channel = connection.channel()
#         channel.exchange_declare(exchange=self._config['exchange'], exchange_type='topic')
#         print('CHANNEL EXCHANGE DECLARE')

#         # This method creates or checks a queue
#         channel.queue_declare(queue=self._queueName)
#         print('CHANNEL QUEUE DECLARE')

#         # Binds the queue to the specified exchang
#         channel.queue_bind(queue=self._queueName,exchange=self._config['exchange'], routing_key=self._bindingKey)
#         channel.basic_consume(queue=self._queueName, on_message_callback=self._on_message_callback, auto_ack=True)
#         print(f"[*] Waiting for data for {self._queueName}. To exit press CTRL+C")

#         try:
#             channel.start_consuming()
#         except KeyboardInterrupt:
#             channel.stop_consuming()


# subscriber = RabbitmqSubscriber('ticker_queue', 'ticker', config)
# ticker_repo = RabbitMqTickerRepository(config, subscriber)
# ticker_service = TickerService(ticker_repo, 1)

# @cbv(router)
# class KlinesRoute:
#     @router.get(f"{API_BASE_URL}/klines")
#     async def get_klines(symbol: str) -> str:
#         topic = RABBITMQ_KLINES_TOPIC
#         # await svc.(topic, symbol)

# @cbv(router)
# class TickerRoute:
#     def __init__(self):
#         print('INIT TICKER ROUTE')
#         # self._ticker_service = ticker_service

@app.post("/push")
async def push_to_connected_websockets(message: str):
    print(message)
    if not notifier.is_ready:
        await notifier.setup("test")
    await notifier.push(f"! Push notification: {message} !")

@app.websocket("/ws/tickers/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str) -> None:
    await notifier.connect(websocket)
    try:
        print('In Webscoket endpoint try')
        while True:
            data = await websocket.receive_text()
            print(data)
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)
# app.include_router(router)


# channel.start_consuming()
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()

    # loop.run_until_complete(create_pool()) 