import typing, time, abc, dataclasses
from typing import Any, Optional
import json, os, asyncio, websockets
import abc
import pandas as pd
import btalib
import mplfinance as mpf
import pika

from binance.client import Client, AsyncClient


# ENVIRONMENTAL VARIABLES
SCHEMA = os.environ.get("SCHEMA")
EXCHANGE = os.environ.get("RABBITMQ_EXCHANGE")
HOST = os.environ.get("RABBITMQ_HOST")
PORT = os.environ.get("RABBITMQ_PORT")
BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_API_SECRET = os.environ.get('BINANCE_API_SECRET')

CURRENCY = 'usdt'
SYMBOLS = [
  "btc", "xrp"  
]


class IPublisher(abc.ABC):       
    @abc.abstractmethod 
    async def publish(self, data: dict) -> None:
        pass

class RabbitmqPublisher(IPublisher):
    """
    RabbitMQ implementation of IPublisher 
    """
    def __init__(self, config):
        self._config = config

    def publish(self, routing_key, message):       
        connection = self._create_connection()
        # Create a new channel with the next available channel number or pass in a channel number to use
        channel = connection.channel()

        # Creates an exchange if it does not already exist, and if the exchange exists,
        # verifies that it is of the correct and expected class. 
        channel.exchange_declare(exchange=self._config['exchange'], exchange_type='topic')
        
        #Publishes message to the exchange with the given routing key
        channel.basic_publish(exchange=self._config['exchange'], routing_key=routing_key, body=message)
        print(f"[x] Sent message {message} for {routing_key}")
        
        connection.close()

    # Create new connection
    def _create_connection(self):
        param = pika.ConnectionParameters(host=self._config['host'], port=self._config['port'], heartbeat=600,
                                       blocked_connection_timeout=300) 
        return pika.BlockingConnection(param)

# INTERFACES / ABSTRACTIONS
class ICryptoStream(abc.ABC):
    @abc.abstractmethod
    async def _coro(self, symbol: str, currency: str) -> None:
        pass

    @abc.abstractmethod
    async def gather_instrument_coros(self) -> None:
        pass

    @abc.abstractmethod
    async def _instrument_async(self, symbol: str, currency: str) -> None:
        pass


class ITicker(abc.ABC):       
    @abc.abstractmethod 
    async def run(self, data: dict) -> None:
        pass

# CONCRETE IMPLEMENTATIONS
class CryptoStream(ICryptoStream):
    """
    Class that receives an injected producer, creates a coroutine per crypto symbol
    by openining a websocket connection to an exchange endpoint 
    and uses the injected producer to push stream data per crypto (per coroutine) to the Kafka topic.
    """
    def __init__(self, ticker: ITicker, exchange: str, instrument: str) -> None:
        self._ticker = ticker
        self._exchange = exchange
        self._instrument = instrument

    async def gather_instrument_coros(self) -> None:
        coros = [self._coro(symbol, CURRENCY) for symbol in SYMBOLS]

        print('22222!!!!!!!!!!!!!!!!!!')
        await asyncio.gather(*coros)

    async def _coro(self, symbol: str, currency: str) -> None:
        await self._instrument_async(symbol, currency)

    async def _instrument_async(self, symbol: str, currency: str) -> None:
        symbol_currency = f"{symbol}{currency}.{self._instrument}"
        print('33333!!!!!!!!!!!!!!!!!!')

        client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_API_SECRET)
        print('111!!!!!!!!!!!!!!!!!!')
        while True: 
            rsi14 = await get_indicators(client)
            msg = {
                "symbol_currency": symbol_currency, 
                "rsi14": rsi14, 
                "timestamp": "timestamp",
                "exchange": self._exchange
            }
            await self._ticker.run(symbol, msg)


class Ticker(ITicker):
    """
    Class that publishes crypto related stream data to a Rabbitmq topic 
    """
    def __init__(self, publisher: IPublisher) -> None:
        self._publisher = publisher

    async def run(self, symbol, message: dict) -> None:
        try:
            # produce message
            print('in ticker')
            value_json = json.dumps(message).encode('utf-8')
            self._publisher.publish(f"{symbol}.rsi14", value_json)
        except Exception as ex:
            time.sleep(1)
            print(ex)

async def get_indicators(client):

    print("IN get_indicators....")
    # client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)#
    asset="BTCUSDT"
    df= pd.DataFrame(await client.get_historical_klines(asset, Client.KLINE_INTERVAL_30MINUTE, "20 Dec, 2021", "08 Jan, 2022"))
    df=df.iloc[:,:6]
    df.columns=["Date","Open","High","Low","Close","Volume"]
    df=df.set_index("Date")
    df.index=pd.to_datetime(df.index,unit="ms")
    df=df.astype("float")
    
    # sma = btalib.sma(df, period=15)
    # df['sma5'] = btalib.sma(df['Close'], period=5).df
    # df['sma20'] = btalib.sma(df['Close'], period=20).df
    # df['sma50'] = btalib.sma(df['Close'], period=50).df
    df['rsi14'] = btalib.rsi(df['Close'], period=14).df
    # macd = btalib.macd(df['Close'], pfast=20, pslow=50, psignal=13)
  
    # df = df.join(macd.df)

    # sma = btalib.sma(df['Close'])
    # print(df.tail(5))
    
    print(df['rsi14'].tail(1).iloc[1])
    # await client.close_connection()
    return df['rsi14'].tail(1).iloc[1]

async def main():
    client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_API_SECRET)
    print("IN MAIN....")
    while True:
        indicators = await get_indicators(client)
        # await asyncio.sleep(20)
        print(indicators)

# MAIN ENTRYPOINT
if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    instrument='rsi14'
    exchange = "binance"
    config={'exchange': EXCHANGE, 'host': HOST, 'port': PORT}
    publisher = RabbitmqPublisher(config=config)
    ticker = Ticker(publisher)
    stream = CryptoStream(ticker, exchange, instrument)
    # instrument2 = CryptoStream(producer, endpoint, exchange, stream2)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stream.gather_instrument_coros())