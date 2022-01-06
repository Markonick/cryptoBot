import typing, time, abc, dataclasses
from typing import Any, Optional
import json, os, asyncio, websockets
import abc
import pika
import sys
from entities import Tick
from dataclasses import fields
# from infra.rabbitmq_pub import IPublisher, RabbitmqPublisher

# CONSTANTS
CURRENCY = 'usdt'
# SYMBOLS = [
#   "btc"  , "xrp"  , "doge" , "xlm"  , "trx"  , 
#   "eos"  , "ltc"  , "iota", "xmr"  , "link" , 
#   "etn"  , "rdd"  , "strax", "npxs" , "glm"  ,
#   "aave" , "sol"  , "atom" , "cro"  , "ht"   ,
#   "mkr"  , "snx"  , "algo" , "ksm"  , "comp" ,
#   "vgx"  , "ftm"  , "zec"  , "rune" , "cel"  ,
#   "rev"  , "icx"  , "hbar" , "chsb" , "iost" ,
#   "zks"  , "lrc"  , "omg"  , "pax"  , "husd" ,
#   "vet"  , "sc"   , "btt"  , "dash" , "xtz"  ,
#   "bch"  , "bnb"  , "ada"  , "usdt" , "dcn"  ,
#   "tfuel", "xvg"  , "rvn"  , "bat"  , "dot"  ,
#   "theta", "luna" , "neo"  , "ftt"  , "dai"  ,
#   "egld" , "fil"  , "leo"  , "sushi", "dcr"  ,
#   "ren"  , "nexo" , "zrx"  , "okb"  , "waves",
#   "dgb"  , "ont"  , "bnt"  , "nano" , "matic",
#   "xwc"  , "zen"  , "btmx" , "qtum" , "hnt"  ,
#   "KNDC" , "delta", "pib"  , "opt"  , "acdc", 
#   "eth",
# ]
# SYMBOLS = [
#   "btc"  , "xrp"  , "doge" , "xlm"  , "trx"  , 
#   "eos"  , "ltc"  , "iota", "eth"  , "link" , 
#   "ada"  , "rdd"  , "btt", "rvn" , "vet"  , "xvg",
# ]
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
        # print(f"[x] Sent message {message} for {routing_key}")
        
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


# MAIN ENTRYPOINT
if __name__ == '__main__':
    # ENVIRONMENTAL VARIABLES
    SCHEMA = os.environ.get("SCHEMA")
    EXCHANGE = os.environ.get("RABBITMQ_EXCHANGE")
    HOST = os.environ.get("RABBITMQ_HOST")
    PORT = os.environ.get("RABBITMQ_PORT")

    exchange = "binance"
    endpoint = "wss://stream.binance.com:9443/ws"

    instrument = 'ticker'
    interval = "10s"
    stream2 = f"kline_{interval}"
    config={'exchange': EXCHANGE, 'host': HOST, 'port': PORT}
    print(config)
    publisher = RabbitmqPublisher(config=config)
    ticker = Ticker(publisher)
    stream = CryptoStream(ticker, endpoint, exchange, instrument)
    # instrument2 = CryptoStream(producer, endpoint, exchange, stream2)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stream.gather_instrument_coros())
    # loop.run_until_complete(instrument2.gather_instrument_coros())