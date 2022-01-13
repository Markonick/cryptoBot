import typing, time, abc, dataclasses
from typing import Any, Optional
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

async def order(side: str, symbol: str, quantity: 10):
    client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_API_SECRET)
    try:
        if TEST_ORDER:
            order = client.create_test_order(symbol=symbol, side=side, type='MARKET', quantity=quantity)
        else:
            pass
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
    return order

async def place_order(symbol: str, signal: str):
    if signal == None:
        print("NO ORDER, DO NOTHING....")
        order_resp = None
    else:
        print(f"{signal} ORDER, {signal} {signal} {signal}!!!!")
        order_resp = await order(signal, symbol, 10)
        
    print(order_resp)
    return order_resp

async def write_symbol(data) -> None:
    connection = await asyncpg.connect('postgresql://devUser:devUser1@cryptodb:5432/cryptos')  
    async with connection.transaction():
        query = f"""
            INSERT INTO {SCHEMA}.symbol (
                name,
                active
            ) 
            VALUES (
                '{data["name"]}',
                {data["active"]}
            )
            ON CONFLICT (name) DO NOTHING
            """
        await connection.execute(query)

async def get_symbol_id(name) -> int:
    connection = await asyncpg.connect('postgresql://devUser:devUser1@cryptodb:5432/cryptos')  
    async with connection.transaction():
        query = f"""SELECT id from {SCHEMA}.symbol sym WHERE sym.name = $1"""
        return await connection.execute(query, name)
    
async def write_order(order_resp, data) -> None:
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
                timeIInForce,
                type,
                side
            ) 
            VALUES (
                {order_resp["symbol_id"]},
                {order_resp["clientOrder_id"]},
                {order_resp["transactTime"]},
                {order_resp["price"]},
                {order_resp["origQty"]},
                {order_resp["executedQty"]},
                {order_resp["cummulativeQuoteQty"]},
                {order_resp["status"]},
                {order_resp["timeIInForce"]},
                {order_resp["type"]},
                {order_resp["side"]}
            )
        """
        await connection.execute(query)
        query = f"""
            INSERT INTO {SCHEMA}.signal (
                symbol_id,
                order_id,
                value,
                curr_rsi,
                prev_rsi,
                created_at
            ) 
            VALUES (
                {data["symbol_id"]},
                {data["order_id"]},
                '{data["value"]}',
                {data["curr_rsi"]},
                {data["prev_rsi"]},
                {data["created_at"]}
            )
        """
        await connection.execute(query)


async def on_message(message: IncomingMessage):
    with message.process():
        print(" [x] %r:%r" % (message.routing_key, message.body))
        msg = json.loads((message.body).decode('UTF-8'))
        symbol = msg["symbol"]
        await write_symbol({"name": symbol, "active": True})
        signal = msg["signal"]
        created_at = list(json.loads(msg["rsi14"]).keys())[1]
        prev_rsi = list(json.loads(msg["rsi14"]).values())[0]
        curr_rsi = list(json.loads(msg["rsi14"]).values())[1]
        binance_order_resp = await place_order(symbol, signal)
        print(binance_order_resp)
        if TEST_ORDER:
            binance_order_resp = {
                "clientOrder_id": None,
                "transactTime": None,
                "price": None,
                "origQty": None,
                "executedQty": None,
                "cummulativeQuoteQty": None,
                "status": None,
                "timeIInForce": None,
                "type": None,
                "side": None
            }
        binance_order_resp["symbol_id"] = await get_symbol_id(symbol)

        if TEST_ORDER:
            order_id = -1
        if signal == None:
            signal = "NOTRANSACTION"
        symbol_id = 1
        # if signal != None:#
        
        data = {
            "symbol_id": symbol_id,
            "order_id": order_id,
            "value": signal,
            "curr_rsi": curr_rsi,
            "prev_rsi": prev_rsi,
            "created_at": created_at,
        }

        await write_order(binance_order_resp, data)

        
async def main(loop):
    # Perform connection
    time.sleep(20)
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
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))

    # we enter a never-ending loop that waits for
    # data and runs callbacks whenever necessary.
    print(" [*] Waiting for messages. To exit press CTRL+C")
    loop.run_forever()
    
    # loop.run_until_complete(main(loop))