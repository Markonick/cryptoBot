import csv, os
from datetime import datetime
from typing import Any
from binance.client import AsyncClient

BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_API_SECRET = os.environ.get('BINANCE_API_SECRET')

columns = [
    'open_time', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
    'ignore'
]

class CsvWriter:
    def __init__(self, datafile: str, symbol: str, timeframe: str):
        self._datafile = datafile
        self._symbol = symbol
        self._timeframe = timeframe

    async def execute(self, start, end):
        started = datetime.now()
        print(f"Starting at: {started}")
        client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_API_SECRET)
        klines = await client.get_historical_klines(self._symbol, client.KLINE_INTERVAL_1MINUTE, start, end)
        print('Starting to get data from binance....')
        with open(self._datafile, 'w', newline='') as f:
            klines_writer = csv.writer(f, delimiter=',')
            klines_writer.writerow(columns)
            for candlestick in klines:
                candlestick[0] = candlestick[0] / 1000 # divide timestamp to ignore miliseconds
                klines_writer.writerow(candlestick)
        
        ended = datetime.now()
        print(f"Ending at: {ended}")

