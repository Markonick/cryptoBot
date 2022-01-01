import os, json
from abc import ABC, abstractmethod
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import LeaderNotAvailableError
from aiokafka.structs import TopicPartition
import asyncpg

from entities import Tick


SCHEMA = os.environ.get("SCHEMA")
KAFKA_ADVERTISED_HOST_NAME = os.environ.get("KAFKA_ADVERTISED_HOST_NAME")
KAFKA_TICKER_TOPIC = os.environ.get("KAFKA_TICKER_TOPIC")
KAFKA_KLINES_TOPIC = os.environ.get("KAFKA_KLINES_TOPIC")

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

class KafkaTickerRepository(ITickerRepository):
    def __init__ (self, loop, topic, host_name: str) -> None:
        self._loop = loop
        self._topic = topic
        self._host_name = host_name

    async def get_ticker_by_window(self, window, symbol=None) -> Tick:

        consumer = AIOKafkaConsumer(
            self._topic,
            loop=self._loop,
            bootstrap_servers=self._host_name,
            enable_auto_commit=False,
            key_deserializer=lambda key: key.decode("utf-8") if key else "",
        )

        await consumer.start()

        while True:
            print('Kafka Consumer started .............')
            try:
                print('INSIDE TRY')
                
                # Consume messages
                msg = await consumer.getone()
                tp = TopicPartition(msg.topic, msg.partition)

                consumer.seek(tp, 1)
                msg2 = await consumer.getone()

                json_msg = json.loads(msg)
                print(json_msg)
                if json_msg["s"] != None and json_msg["s"].lower() == symbol.lower():
                    return msg
            except Exception as e:
                print(e)
            finally:
                # Will leave consumer group; perform autocommit if enabled.
                await consumer.stop()