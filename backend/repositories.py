import os, json
from abc import ABC, abstractmethod
import asyncpg
import pika
import sys

from entities import Tick

def get_tick_query(event_time):
    return f"""
        SELECT *
        FROM  {SCHEMA}.tick
        WHERE event_time < {event_time}
        ORDER BY event_time DESC
        LIMIT 1;
    """

class ITickerRepository(ABC):
    @abstractmethod
    async def get_ticker_by_window(self, window) -> Tick:
        pass

class DbTickerRepository(ITickerRepository):
    def __init__(self):
        pass

    async def get_ticker_by_window(self, window, symbol=None) -> Tick:
        conn = await asyncpg.connect('postgres://devUser:devUser1@cryptodb:5432/cryptos')  
        tick = await conn.fetch(get_tick_query(window))

        return tick

class RabbitMqTickerRepository(ITickerRepository):
    def __init__ (self, config, subscriber) -> None:
        self._config = config
        self._subscriber = subscriber
        self._subscriber.consume()
        
    async def get_ticker_by_window(self) -> Tick:
        
        print('GET TICKER')
        print('CONSUMING QUEUE//..')
        # return self._subscriber.get_msg()
        # while True:
        #     print('RABBITMQ Consumer started .............')
        #     try:
        #         print('INSIDE TRY')
                
        #         # Consume messages
        #         msg = await consumer.getone()
        #         tp = TopicPartition(msg.topic, msg.partition)

        #         consumer.seek(tp, 1)
        #         msg2 = await consumer.getone()

        #         json_msg = json.loads(msg)
        #         print(json_msg)
        #         if json_msg["s"] != None and json_msg["s"].lower() == symbol.lower():
        #             return msg
        #     except Exception as e:
        #         print(e)
        #     finally:
        #         # Will leave consumer group; perform autocommit if enabled.
        #         await consumer.stop()