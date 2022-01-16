import os, json
from abc import ABC, abstractmethod
import asyncpg
import pika
import sys
import dataclasses
from typing import TypeVar, Type, List
from entities import Tick, OrderDetails

SCHEMA = os.environ.get("SCHEMA")

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

def is_dataclass_type(typ) -> bool:
    "True if the argument corresponds to a data class type (but not an instance)."

    return isinstance(typ, type) and dataclasses.is_dataclass(typ)

T = TypeVar("T")
def _typed_fetch(typ: Type[T], records: List[asyncpg.Record]) -> List[T]:
    results = []
    for record in records:
        result = object.__new__(typ)
        if is_dataclass_type(typ):
            for field in dataclasses.fields(typ):
                key = field.name
                value = record.get(key, None)
                if value is not None:
                    setattr(result, key, value)
                # elif field.default:
                #     setattr(result, key, field.default)
                # else:
                #     raise RuntimeError(
                #         f"object field {key} without default value is missing a corresponding database record column"
                #     )
        else:
            for key, value in record.items():
                setattr(result, key, value)

        results.append(result)
    return results
    
class OrdersRepository():
    def __init__(self):
        pass

    async def get_orders_count(self) -> int:
        connection = await asyncpg.connect('postgres://devUser:devUser1@cryptodb:5432/cryptos')

        query = f"""
            SELECT count(*) from {SCHEMA}.order 
        """
        count = await connection.fetchval(query)
        return count

    async def get_all_orders(self, page_size: int, page_number: int) -> OrderDetails:
        connection = await asyncpg.connect('postgres://devUser:devUser1@cryptodb:5432/cryptos')
        offset = str((page_number) * page_size)
        limit = str(page_size)
        print(offset)
        print(limit)
        query = f"""
            SELECT * from {SCHEMA}.order ord
            JOIN {SCHEMA}.signal sig on ord.id = sig.order_id
            OFFSET {offset} LIMIT {limit}
        """
        result = await connection.fetch(query)
        orders = _typed_fetch(OrderDetails, result)
        return orders
