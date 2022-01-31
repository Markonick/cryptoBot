import csv, os, asyncio, time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Generator, List
from binance.client import Client, AsyncClient
from binance.exceptions import BinanceAPIException, BinanceOrderException
from contextlib import asynccontextmanager

BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_API_SECRET = os.environ.get('BINANCE_API_SECRET')

columns = [
    'open_time', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
    'ignore'
]
SYMBOLS = [
    'BTCUSDT', 'XRPUSDT', 'DOGEUSDT', 'XLMUSDT', 'TRXUSDT', 'EOSUSDT', 'LTCUSDT', 'MIOTAUSDT', 'XMRUSDT', 'LINKUSDT', 
    'ETNUSDT', 'RDDUSDT', 'STRAXUSDT', 'NPXSUSDT', 'GLMUSDT', 'AAVEUSDT', 'SOLUSDT', 'ATOMUSDT', 'CROUSDT', 'HTUSDT', 
    'MKRUSDT', 'SNXUSDT', 'ALGOUSDT', 'KSMUSDT', 'COMPUSDT', 'VGXUSDT', 'FTMUSDT', 'ZECUSDT', 'RUNEUSDT', 'CELUSDT', 
    'REVUSDT', 'ICXUSDT', 'HBARUSDT', 'CHSBUSDT', 'IOSTUSDT', 'ZKSUSDT', 'LRCUSDT', 'OMGUSDT', 'PAXUSDT', 'HUSDUSDT', 
    'VETUSDT', 'SCUSDT', 'BTTUSDT', 'DASHUSDT', 'XTZUSDT', 'BCHUSDT', 'BNBUSDT', 'ADAUSDT', 'DCNUSDT', 'TFUELUSDT', 
    'XVGUSDT', 'RVNUSDT', 'BATUSDT', 'DOTUSDT', 'THETAUSDT', 'LUNAUSDT', 'NEOUSDT', 'FTTUSDT', 'DAIUSDT', 'EGLDUSDT', 
    'FILUSDT', 'LEOUSDT', 'SUSHIUSDT', 'DCRUSDT', 'RENUSDT', 'NEXOUSDT', 'ZRXUSDT', 'OKBUSDT', 'WAVESUSDT', 'DGBUSDT', 
    'ONTUSDT', 'BNTUSDT', 'NANOUSDT', 'MATICUSDT', 'XWCUSDT', 'ZENUSDT', 'BTMXUSDT', 'QTUMUSDT', 'HNTUSDT', 'KNDCUSDT', 
    'DELTAUSDT', 'PIBUSDT', 'OPTUSDT', 'ACDCUSDT', 'ETHUSDT'
]

# Write Python 3 code in this online editor and run it.
from enum import Enum

class Interval(Enum):
    KLINE_INTERVAL_1MINUTE = '1m'
    KLINE_INTERVAL_3MINUTE = '3m'
    KLINE_INTERVAL_5MINUTE = '5m'
    KLINE_INTERVAL_15MINUTE = '15m'
    KLINE_INTERVAL_30MINUTE = '30m'
    KLINE_INTERVAL_1HOUR = '1h'
    KLINE_INTERVAL_2HOUR = '2h'
    KLINE_INTERVAL_4HOUR = '4h'
    KLINE_INTERVAL_6HOUR = '6h'
    KLINE_INTERVAL_8HOUR = '8h'
    KLINE_INTERVAL_12HOUR = '12h'
    KLINE_INTERVAL_1DAY = '1d'
    KLINE_INTERVAL_3DAY = '3d'
    KLINE_INTERVAL_1WEEK = '1w'
    KLINE_INTERVAL_1MONTH = '1M'

# Possible parallelisation params:
# - symbol
# - interval

@asynccontextmanager
async def get_client(api_key, api_secret):
    client = await AsyncClient.create(api_key, api_secret)
    try:
        yield client
    finally:
        await client.close_connection()

class ReadHistoricalData:
    @classmethod
    async def get(cls, symbol: str, interval: str, start_str: str, end_str: str):
        started = datetime.now()
        print(f"API data reading starting at: {started}")
        async with get_client(BINANCE_API_KEY, BINANCE_API_SECRET) as client:
            try:
                klines = await client.get_historical_klines(symbol, interval, start_str, end_str)
                time.sleep(2)
            except BinanceAPIException as e:
                # error handling goes here
                print(f"BinanceAPIException for symbol {symbol}")
                print(e)
                klines = []
            except BinanceOrderException as e:
                # error handling goes here
                print(f"BinanceOrderException for symbol {symbol}")
                print(e)
                klines = []
            finally:
                ended = datetime.now()
                print(f"API data reading ending at: {ended}")
            return BinanceStructure(data=klines, symbol=symbol)

@dataclass
class BinanceStructure:
    data: List[Any]
    symbol: str

class WriteHistoricalData:
    @classmethod
    async def execute(cls, binance_data_model: BinanceStructure, interval: str, start_str: str, end_str: str):
        #BTCUSDT-2017-2020-12h.csv
        datafile = f"data/{binance_data_model.symbol}-{start_str.replace('-','')}-{end_str.replace('-','')}-{interval}.csv"
        with open(datafile, 'w', newline='') as f:
            klines_writer = csv.writer(f, delimiter=',')
            klines_writer.writerow(columns)
            # klines_writer.writerows(binance_data_model.data)
            for candlestick in binance_data_model.data:
                candlestick[0] = int(candlestick[0] / 1000) # divide timestamp to ignore miliseconds
                candlestick[6] = int(candlestick[6] / 1000) # divide timestamp to ignore miliseconds
                klines_writer.writerow(candlestick)
        ended = datetime.now()
        print(f"Ending at: {ended}")

async def gather_coros(symbols: List[str], interval: str, start_str: str, end_str: str) -> None:
    started = datetime.now()
    print(f"Starting at: {started}")

    read_symbols_data = [await ReadHistoricalData.get(symbol, interval, start_str, end_str) for symbol in symbols]
    write_coros = [WriteHistoricalData.execute(result, interval, start_str, end_str) for result in read_symbols_data]
    await asyncio.gather(*write_coros)

# MAIN ENTRYPOINT
if __name__ == '__main__':
    now = datetime.now()
    symbols = ['BTCUSDT', 'XRPUSDT', 'ETHUSDT', 'DOGEUSDT']
    interval = '30m'
    start = '2017-01-01'
    end = '2022-01-29'
    asyncio.run(gather_coros(symbols, interval, start, end))