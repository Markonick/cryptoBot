import csv, os
from binance.client import AsyncClient

BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_API_SECRET = os.environ.get('BINANCE_API_SECRET')
dataStart = '1 Jan, 2021'
dataEnd = '2 Jan, 2021'
datafile = 'data/BTCUSDT-20210101-20210102-1m.csv'

columns = [
    'open_time', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
    'ignore'
]

class CsvWriter:
    def __init__(self, datafile, symbol):
        self._datafile = datafile
        self._symbol = symbol

    async def execute(self, start, end):  
        client = await AsyncClient.create(BINANCE_API_KEY, BINANCE_API_SECRET)
        klines = await client.get_historical_klines(self._symbol, client.KLINE_INTERVAL_1MINUTE, start, end)

        with open(self._datafile, 'w', newline='') as f:
            klines_writer = csv.writer(f, delimiter=',')
            klines_writer.writerow(columns)
            klines_writer.writerows(klines)

