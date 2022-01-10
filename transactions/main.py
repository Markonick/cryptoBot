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
        order = client.create_test_order(symbol=symbol, side=side, type='MARKET', quantity=quantity)
    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        print(e)
    return order

def place_order(symbol: str, signal: str):
    if signal == None:
        print("NO ORDER, DO NOTHING....")
        order_resp = None
    else:
        print(f"{signal} ORDER, {signal} {signal} {signal}!!!!")
        order_resp = order(signal, symbol, 10)
        
    print(order_resp)

def insert_signal_query(data):
    return f"""
        INSERT INTO {SCHEMA}.tick (
            id,
            symbol_id,
            signal,
            created_at,
            rsi,
            prev_rsi,
            prev_created_at,
        ) 
        VALUES (
            {data["id"]},
            {data["symbol_id"]},
            {data["signal"]},
            {data["created_at"]},
            {data["rsi"]},
            {data["prev_rsi"]},
            {data["prev_created_at"]}
        )
    """

def insert_order_query(data):
    return f"""
        INSERT INTO {SCHEMA}.tick (
            id,
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
            side,
        ) 
        VALUES (
            {data["id"]},
            {data["symbol_id"]},
            {data["clientOrder_id"]},
            {data["transactTime"]},
            {data["price"]},
            {data["origQty"]},
            {data["executedQty"]},
            {data["cummulativeQuoteQty"]},
            {data["status"]},
            {data["I"]},
            {data["type"]},
            {data["side"]},
        )
    """

async def write_order(data) -> None:
    connection = await asyncpg.connect('postgres://devUser:devUser1@cryptodb:5432/cryptos')  
    async with connection.transaction():
        await connection.execute(insert_order_query(data))

async def write_signal(data) -> None:
    connection = await asyncpg.connect('postgres://devUser:devUser1@cryptodb:5432/cryptos')  
    async with connection.transaction():
        await connection.execute(insert_signal_query(data))

async def on_message(message: IncomingMessage):
    with message.process():
        print(" [x] %r:%r" % (message.routing_key, message.body))
        msg = json.loads((message.body).decode('UTF-8'))
        symbol = msg["symbol"]
        signal = msg["signal"]
        prev_created_at = list(json.loads(msg["rsi14"]).keys())[0]
        created_at = list(json.loads(msg["rsi14"]).keys())[1]
        prevRsi = list(json.loads(msg["rsi14"]).values())[0]
        curRsi = list(json.loads(msg["rsi14"]).values())[1]
        place_order(symbol, signal)
        # if signal != None:
        data = {
            "symbol_id": 1,
            "signal": signal,
            "created_at": created_at,
            "rsi": curRsi,
            "prev_rsi": prevRsi,
            "prev_created_at": prev_created_at,
        }
        await write_signal(data)

        
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