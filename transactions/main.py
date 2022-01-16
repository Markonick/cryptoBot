import typing, time, abc
from dataclasses import dataclass
from typing import Any, Optional, List
import json, os, asyncio, websockets
import sys
import asyncpg
from aio_pika import connect, IncomingMessage, ExchangeType

import abc
from datetime import datetime, timedelta
import pandas as pd
import btalib
import mplfinance as mpf

from binance.client import Client, AsyncClient
from binance.exceptions import BinanceAPIException, BinanceOrderException


# ENVIRONMENTAL VARIABLES
SCHEMA = os.environ.get("SCHEMA")
TEST_ORDER = os.environ.get("TEST_ORDER")
EXCHANGE = os.environ.get("RABBITMQ_EXCHANGE")
HOST = os.environ.get("RABBITMQ_HOST")
PORT = os.environ.get("RABBITMQ_PORT")
BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_API_SECRET = os.environ.get('BINANCE_API_SECRET')
SYMBOLS = [
  "BTCUSDT", "XRPUSDT"  
]

async def order(side: str, symbol: str, quantity: int ): # Need to calculate quantity!! Also there is a MI_NOTIONAL exception (BinanceAPIException) if quantity wrong!!
    client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_API_SECRET)
    order = {}
    try:
        if TEST_ORDER:
            order = await client.create_test_order(symbol=symbol, side=side, type='MARKET', quantity=quantity) 
        else:
            pass
    except BinanceAPIException as e:
        # error handling goes here
        print('BinanceAPIException')
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        print('BinanceOrderException')
        print(e)

      
    await client.close_connection()
    return order

async def place_order(symbol: str, signal: str):
    print(f"{signal} ORDER, {signal} {signal} {signal}!!!!")
    order_resp = await order(signal, symbol, 100)
        
    return order_resp

async def write_symbol(data) -> None:
    connection = await asyncpg.connect('postgresql://devUser:devUser1@cryptodb:5432/cryptos')  
    async with connection.transaction():
        query = f"""
            INSERT INTO {SCHEMA}.symbol (
                name,
                active
            ) 
            VALUES ( $1, $2 )
            ON CONFLICT (name) DO NOTHING
            """
        await connection.execute(query, *data)

async def get_symbol_id(name) -> int:
    connection = await asyncpg.connect('postgresql://devUser:devUser1@cryptodb:5432/cryptos')  
    async with connection.transaction():
        query = f"""SELECT sym.id from {SCHEMA}.symbol sym WHERE sym.name = $1"""
        symbol_id = await connection.fetchval(query, name)
        return symbol_id

async def get_order_id() -> int:
    connection = await asyncpg.connect('postgresql://devUser:devUser1@cryptodb:5432/cryptos')  
    async with connection.transaction():
        query = f"""SELECT ord.id from {SCHEMA}.order ord ORDER BY id DESC LIMIT 1"""
        order_id = await connection.fetchval(query)
        return order_id

@dataclass
class Symbol:
    name: str
    active: bool
    
    @property
    def as_db_args(self) -> List:
        return [self.name, self.active]

@dataclass
class BinanceOrderResponse:
    symbol_id: int
    clientOrder_id: Optional[int] = None
    transactTime: Optional[int] = None
    price: Optional[float] = None
    origQty: Optional[int] = None
    executedQty: Optional[int] = None
    cummulativeQuoteQty: Optional[int] = None
    status: Optional[str] = None
    timeInForce: Optional[str] = None
    type: Optional[str] = None
    side: Optional[str] = None

    @property
    def as_db_args(self) -> List:
        return [
            self.symbol_id, self.clientOrder_id, self.transactTime, self.price, self.origQty, self.executedQty, 
            self.cummulativeQuoteQty, self.status, self.timeInForce, self.type, self.side
        ]

@dataclass
class Signal:
    symbol_id: int
    order_id: int
    value: str
    curr_rsi: float
    prev_rsi: float
    created_at: int

    @property
    def as_db_args(self) -> List:
        return [self.symbol_id, self.order_id, self.value, self.curr_rsi, self.prev_rsi, self.created_at]


async def write_order(order_resp: BinanceOrderResponse, data: Signal) -> None:
    connection = await asyncpg.connect('postgresql://devUser:devUser1@cryptodb:5432/cryptos')  
    async with connection.transaction():
        # if not TEST_ORDER:
        query = f"""
            INSERT INTO {SCHEMA}.order (
                symbol_id,
                clientOrder_id,
                transactTime,
                price,
                origQty,
                executedQty,
                cummulativeQuoteQty,
                status,
                timeInForce,
                type,
                side
            ) 
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """

        await connection.execute(query, *order_resp)

        query = f"""
            INSERT INTO {SCHEMA}.signal (
                symbol_id,
                order_id,
                value,
                curr_rsi,
                prev_rsi,
                created_at
            ) 
            VALUES ($1, $2, $3, $4, $5, $6)
        """
        
        await connection.execute(query, *data)


async def on_message(message: IncomingMessage):
    with message.process():
        print(" [x] %r:%r" % (message.routing_key, message.body))
        msg = json.loads((message.body).decode('UTF-8'))
        symbol_name = msg["symbol"]
        symbol_data = Symbol(name=symbol_name, active=True)
        await write_symbol(symbol_data.as_db_args)
        signal = msg["signal"]
        created_at = json.loads(list(json.loads(msg["rsi14"]).keys())[1])
        prev_rsi = list(json.loads(msg["rsi14"]).values())[0]
        curr_rsi = list(json.loads(msg["rsi14"]).values())[1]
        signal = "BUY"
        curr_rsi = 29
        if signal != None:
            binance_order_resp = await place_order(symbol_name, signal) # What is this? and why do we repopulate it 3 lines down?
            if TEST_ORDER:
                symbol_id = await get_symbol_id(symbol_name)
                binance_order_resp = BinanceOrderResponse(symbol_id=symbol_id) # What is this? and why do we populate it 3 lines up?
            order_id = await get_order_id()
            symbol_id = 1
            signal_data = Signal(symbol_id=symbol_id, order_id=order_id, value=signal, curr_rsi=curr_rsi, prev_rsi=prev_rsi, created_at=created_at) 

            await write_order(binance_order_resp.as_db_args, signal_data.as_db_args)
        else:       
            print("NO ORDER, DO NOTHING....")
            binance_order_resp = None
            signal = "NOTRANSACTION"
            
   
async def main(loop):
    # Perform connection
    connection = await connect(
        "amqp://guest:guest@rabbitmq/", loop=loop
    )

    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    # Declare an exchange
    rsi_exchange = await channel.declare_exchange(
        EXCHANGE, ExchangeType.TOPIC
    )

    # Declaring queues
    for i, symbol in enumerate(SYMBOLS):
        queue = await channel.declare_queue(
            f"indicators.rsi14", auto_delete=True
        )

        await queue.bind(rsi_exchange, routing_key=f"indicators.rsi14")
        await queue.consume(on_message,)
        is_ready = True

    # Start listening the queue with name 'task_queue'
    await queue.consume(on_message)


if __name__ == "__main__":
    time.sleep(20)
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))

    # we enter a never-ending loop that waits for
    # data and runs callbacks whenever necessary.
    print(" [*] Waiting for messages. To exit press CTRL+C")
    loop.run_forever()