import typing, time, json, os, asyncio
from abc import ABC, abstractmethod
from typing import Optional, NewType
from fastapi import FastAPI, WebSocket, Depends, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from starlette.middleware.cors import CORSMiddleware
import pika
import asyncpg

from repositories import RabbitMqTickerRepository
from services import TickerService

class ISubscriber(ABC):       
    @abstractmethod 
    async def consume(self, data: dict) -> None:
        pass

class RabbitmqSubscriber(ISubscriber):
    """
    RabbitMQ implementation of IPublisher 
    """
    def __init__(self, queueName, bindingKey, config):
      self._queueName = queueName
      self._bindingKey = bindingKey
      self._config = config
      print(self._config)
      self._connection = self._create_connection()
  
    # def __del__(self):
    #     self._connection.close()

    def _create_connection(self):
        parameters = pika.ConnectionParameters(host=self._config['host'], port = self._config['port'])
        return pika.BlockingConnection(parameters)

    def _on_message_callback(self, channel, method, properties, body):
        binding_key = method.routing_key
        # print(f"received new message for - {binding_key}")
 
        print(" [x] Received %r" % body)
        time.sleep(body.count(b'.'))
        print(" [x] Done")

        print('==========JSON.LOADS: =============')
        json_loads_msg = json.loads(body)
        print(json_loads_msg)
        self._msg = json_loads_msg

        channel.basic_ack(delivery_tag = method.delivery_tag)
    
    def get_msg(self):
        return self._msg
        
    def consume(self):
        
        channel = self._connection.channel()
        channel.exchange_declare(exchange=self._config['exchange'], exchange_type='topic')
        print('CHANNEL EXCHANGE DECLARE')

        # This method creates or checks a queue
        channel.queue_declare(queue=self._queueName)
        print('CHANNEL QUEUE DECLARE')

        # Binds the queue to the specified exchang
        channel.queue_bind(queue=self._queueName,exchange=self._config['exchange'], routing_key=self._bindingKey)
        channel.basic_consume(queue=self._queueName, on_message_callback=self._on_message_callback, auto_ack=True)
        print(f"[*] Waiting for data for {self._queueName}. To exit press CTRL+C")

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()

SCHEMA = os.environ.get("SCHEMA")
EXCHANGE = os.environ.get("RABBITMQ_EXCHANGE")
HOST = os.environ.get("RABBITMQ_HOST")
PORT = os.environ.get("RABBITMQ_PORT")
RABBITMQ_KLINES_TOPIC = os.environ.get("RABBITMQ_KLINES_TOPIC")
config={'exchange': EXCHANGE, 'host': HOST, 'port': PORT}

API_BASE_URL = os.environ.get("API_BASE_URL")

app = FastAPI()
router = InferringRouter()
app.add_middleware(CORSMiddleware, allow_origins=["*"])
loop = asyncio.get_event_loop()

subscriber = RabbitmqSubscriber('ticker_queue', 'ticker', config)
ticker_service = TickerService(RabbitMqTickerRepository(config, subscriber), 1)
@cbv(router)
class KlinesRoute:
    @router.get(f"{API_BASE_URL}/klines")
    async def get_klines(symbol: str) -> str:
        topic = RABBITMQ_KLINES_TOPIC
        # await svc.(topic, symbol)

@cbv(router)
class TickerRoute:
    def __init__(self):
        print('INIT TICKER ROUTE')
        self._ticker_service = ticker_service

    @router.websocket("/ws/tickers/{symbol}")
    async def websocket_endpoint(self, websocket: WebSocket, symbol: str) -> None:
        print('WAITING FOR CONNECTION.......')
        await websocket.accept()
        print("WEBSOCKET ACCEPTED")
        msg = {"Message: ": "connected"}
        await websocket.send_json(msg)
        print("WEBSOCKET send_json")
        tick = await self._ticker_service.get_ticker(symbol)
        print("WEBSOCKET awaiting send_text")
        await websocket.send_text(tick)

app.include_router(router)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(create_pool()) 