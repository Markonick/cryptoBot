import typing, time, abc, dataclasses
from typing import Any, Optional
import json, os, asyncio, websockets
import abc
import pandas as pd
import btalib
import mplfinance as mpf
import pika

from binance.client import Client, AsyncClient

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
        self._connection = self._create_connection()

    def publish(self, routing_key, message):    
        # Create a new channel with the next available channel number or pass in a channel number to use
        channel = self._connection.channel()

        # Creates an exchange if it does not already exist, and if the exchange exists,
        # verifies that it is of the correct and expected class. 
        channel.exchange_declare(exchange=self._config['exchange'], exchange_type='topic')
        
        #Publishes message to the exchange with the given routing key
        channel.basic_publish(exchange=self._config['exchange'], routing_key=routing_key, body=message)
        print(f"[x] Sent message {message} for {routing_key}")

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
    async def _websocket_instrument_async(self, symbol: str, currency: str) -> None:
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
    def __init__(self, ticker: ITicker, endpoint: str, exchange: str, instrument: str) -> None:
        self._ticker = ticker
        self._endpoint = endpoint
        self._exchange = exchange
        self._instrument = instrument

    async def gather_instrument_coros(self) -> None:
        coros = [self._coro(symbol, CURRENCY) for symbol in SYMBOLS]
        await asyncio.gather(*coros)

    async def _coro(self, symbol: str, currency: str) -> None:
        await self._websocket_instrument_async(symbol, currency)

    async def _websocket_instrument_async(self, symbol: str, currency: str) -> None:
        subscribe = json.dumps({"method": "SUBSCRIBE", "params": [f"{symbol}{currency}@{self._instrument}"], "id": 1})
        async with websockets.connect(self._endpoint) as websocket:
            await websocket.send(subscribe)

            while True:
                data = await websocket.recv()
                data_json = json.loads(data)

                if 'result' not in data_json:
                    msg = {**data_json, "exchange": self._exchange}
                    await self._ticker.run(msg)


class Ticker(ITicker):
    """
    Class that publishes crypto related stream data to a Rabbitmq topic 
    """
    def __init__(self, publisher: IPublisher) -> None:
        self._publisher = publisher

    async def run(self, message: dict) -> None:
        try:
            # produce message
            value_json = json.dumps(message).encode('utf-8')
            self._publisher.publish('ticker', value_json)
        except Exception as ex:
            time.sleep(1)
            print(ex)

async def main():
    # ENVIRONMENTAL VARIABLES
    SCHEMA = os.environ.get("SCHEMA")
    EXCHANGE = os.environ.get("RABBITMQ_EXCHANGE")
    HOST = os.environ.get("RABBITMQ_HOST")
    PORT = os.environ.get("RABBITMQ_PORT")

    BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
    BINANCE_API_SECRET = os.environ.get('BINANCE_API_SECRET')

    # client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)#
    client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_API_SECRET)
    print(await client.ping())
    asset="BTCUSDT"
    start="2021.10.1"
    end="2021.12.1"
    timeframe="1d"
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    df=pd.DataFrame(await client.get_all_tickers())
    df=df.set_index("symbol")
    df["price"]=df["price"].astype("float")
    df.index=df.index.astype("string")
    # print(df)
    print(df.loc["BTCUSDT"])
    df= pd.DataFrame(await client.get_historical_klines(asset, Client.KLINE_INTERVAL_30MINUTE, "1 Sept, 2021", "29 Dec, 2021"))
    df=df.iloc[:,:6]
    df.columns=["Date","Open","High","Low","Close","Volume"]
    df=df.set_index("Date")
    df.index=pd.to_datetime(df.index,unit="ms")
    df=df.astype("float")
    
    sma = btalib.sma(df, period=15)
    df['sma5'] = btalib.sma(df['Close'], period=5).df
    df['sma20'] = btalib.sma(df['Close'], period=20).df
    df['sma50'] = btalib.sma(df['Close'], period=50).df
    df['rsi14'] = btalib.rsi(df['Close'], period=14).df
    macd = btalib.macd(df['Close'], pfast=20, pslow=50, psignal=13)
  
    df = df.join(macd.df)

    # sma = btalib.sma(df['Close'])
    print(df.tail(5))
    await client.close_connection()
# MAIN ENTRYPOINT
if __name__ == '__main__':

    # mpf.plot(df, type='candle', volume=True, mav=7)
    # exchange = "binance"
    # endpoint = "wss://stream.binance.com:9443/ws"

    # stream1 = 'ticker'
    # interval = "1s"
    # stream2 = f"kline_{interval}"
    # config={'exchange': EXCHANGE, 'host': HOST, 'port': PORT}
    # print(config)
    # publisher = RabbitmqPublisher(config=config)
    # ticker = Ticker(publisher)
    # stream1 = CryptoStream(ticker, endpoint, exchange, stream1)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(stream1.gather_instrument_coros())


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())