import typing, time, abc, dataclasses
from typing import Any, Optional
import json, os, asyncio, websockets
import sys
from aio_pika import connect, IncomingMessage, ExchangeType

import abc
from datetime import datetime, timedelta
import pandas as pd
import btalib
import mplfinance as mpf

from binance.client import Client, AsyncClient


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

async def buy_order():
    client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_API_SECRET)
    return client.create_test_order(symbol='XRPUSDT', side='BUY', type='MARKET', quantity=10)

async def sell_order():
    client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_API_SECRET)
    return client.create_test_order(symbol='XRPUSDT', side='SELL', type='MARKET', quantity=10)

def place_order(signal: str):
    if signal == "SELL":
        print("SELL ORDER, SELL SELL SELL!!!!")
        sell_order()
    elif signal == "BUY":
        print("BUY ORDER, BUY BUY BUY!!!!")
        buy_order()
    else:
        print("NO ORDER, DO NOTHING....")
        pass

def on_message(message: IncomingMessage):
    with message.process():
        print(" [x] %r:%r" % (message.routing_key, message.body))
        msg = json.loads((message.body).decode('UTF-8'))
        signal = msg["signal"]
        print(signal)
        place_order(signal)
        
async def main(loop):
    # Perform connection
    print('000000000000000')
    await asyncio.sleep(10)
    connection = await connect(
        "amqp://guest:guest@rabbitmq/", loop=loop
    )

    print('11111111111111111')
    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    print('2222222222222222222')
    # Declare an exchange
    rsi_exchange = await channel.declare_exchange(
        EXCHANGE, ExchangeType.TOPIC
    )

    print('33333333333333333333')
    # Declaring queues
    for i, symbol in enumerate(SYMBOLS):
        queue = await channel.declare_queue(
            f"indicators.rsi14", auto_delete=True
        )

        await queue.bind(rsi_exchange, routing_key=f"indicators.rsi14")
        await queue.consume(on_message,)
        print(f"after {symbol} queue consume")
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