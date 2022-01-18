from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import backtrader as bt # Import the backtrader platfor#
import csv, os, asyncio, time
from csv_writer import CsvWriter


# Create a Stratey
class SMAStrategy(bt.Strategy):

    params = (
        ('maperiod', None),
        ('quantity', None)
    )


    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.amount = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

        self.order = None


    def next(self):

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # Keep track of the created order to avoid a 2nd order
                self.amount = (self.broker.getvalue() * self.params.quantity) / self.dataclose[0]
                self.order = self.buy(size=self.amount)
        else:
            # Already in the market ... we might sell
            if self.dataclose[0] < self.sma[0]:

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=self.amount)



class RSIStrategy(bt.Strategy):

    params = (
        ('maperiod', None),
        ('quantity', None)
    )


    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.amount = None

        # Add a MovingAverageSimple indicator
        self.rsi = bt.talib.RSI(self.datas[0], timeperiod=self.params.maperiod)


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

        self.order = None


    def next(self):

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.rsi < 30:

                # Keep track of the created order to avoid a 2nd order
                self.amount = (self.broker.getvalue() * self.params.quantity) / self.dataclose[0]
                self.order = self.buy(size=self.amount)
        else:
            # Already in the market ... we might sell
            if self.rsi > 70:

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=self.amount)
                

# ______________________ End Strategy Class



def timeFrame(datapath):
    """
    Select the write compression and timeframe.
    """
    sepdatapath = datapath[5:-4].split(sep='-') # ignore name file 'data/' and '.csv'
    tf = sepdatapath[3]

    if tf == '1mth':
        compression = 1
        timeframe = bt.TimeFrame.Months
    elif tf == '12h':
        compression = 720
        timeframe = bt.TimeFrame.Minutes
    elif tf == '15m':
        compression = 15
        timeframe = bt.TimeFrame.Minutes
    elif tf == '30m':
        compression = 30
        timeframe = bt.TimeFrame.Minutes
    elif tf == '1d':
        compression = 1
        timeframe = bt.TimeFrame.Days
    elif tf == '1h':
        compression = 60
        timeframe = bt.TimeFrame.Minutes
    elif tf == '3m':
        compression = 3
        timeframe = bt.TimeFrame.Minutes
    elif tf == '2h':
        compression = 120
        timeframe = bt.TimeFrame.Minutes
    elif tf == '3d':
        compression = 3
        timeframe = bt.TimeFrame.Days
    elif tf == '1w':
        compression = 1
        timeframe = bt.TimeFrame.Weeks
    elif tf == '4h':
        compression = 240
        timeframe = bt.TimeFrame.Minutes
    elif tf == '5m':
        compression = 5
        timeframe = bt.TimeFrame.Minutes
    elif tf == '6h':
        compression = 360
        timeframe = bt.TimeFrame.Minutes
    elif tf == '8h':
        compression = 480
        timeframe = bt.TimeFrame.Minutes
    else:
        print('dataframe not recognized')
        exit()
    
    return compression, timeframe


def getWinLoss(analyzer):
    return analyzer.won.total, analyzer.lost.total, analyzer.pnl.net.total


def getSQN(analyzer):
    return round(analyzer.sqn,2)



def runbacktest(datapath, start, end, period, strategy, commission_val=None, portofolio=10000.0, stake_val=1, quantity=0.01, plt=False):

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=stake_val) # Multiply the stake by X

    cerebro.broker.setcash(portofolio) # default : 10000.0

    if commission_val:
        cerebro.broker.setcommission(commission=commission_val/100) # divide by 100 to remove the %

    # Add a strategy
    if strategy == 'SMA':
        cerebro.addstrategy(SMAStrategy, maperiod=period, quantity=quantity)
    elif strategy == 'RSI':
        cerebro.addstrategy(RSIStrategy, maperiod=period, quantity=quantity)
    else :
        print('no strategy')
        exit()

    compression, timeframe = timeFrame(datapath)
    # Create a Data Feed
    data = bt.feeds.GenericCSVData(
        dataname = datapath,
        dtformat = 2, 
        compression = compression, 
        timeframe = timeframe,
        fromdate = datetime.datetime.strptime(start, '%Y-%m-%d'),
        todate = datetime.datetime.strptime(end, '%Y-%m-%d'),
        reverse = False)


    # Add the Data Feed to Cerebro
    cerebro.adddata(data)


    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

    strat = cerebro.run()
    stratexe = strat[0]

    try:
        totalwin, totalloss, pnl_net = getWinLoss(stratexe.analyzers.ta.get_analysis())
    except KeyError:
        totalwin, totalloss, pnl_net = 0, 0, 0

    sqn = getSQN(stratexe.analyzers.sqn.get_analysis())


    if plt:
        cerebro.plot()

    return cerebro.broker.getvalue(), totalwin, totalloss, pnl_net, sqn

async def run_strategy(strategy, symbol, periodRange, start, end, timeframe):
    now = datetime.datetime.now().isoformat("_","seconds")
    #BTCUSDT-2017-2020-12h.csv
    datafile = f"data/{symbol}-{start.split('-')[0]}-{end.split('-')[0]}-{timeframe}.csv"
    writer = CsvWriter(datafile, symbol)
    await writer.execute(start, end)
    # time.sleep(20)
    for data in os.listdir("./data"):
        datapath = 'data/' + data
        sep = datapath[5:-4].split(sep='-') # ignore name file 'data/' and '.csv'
        # sep[0] = pair; sep[1] = year start; sep[2] = year end; sep[3] = timeframe

        print('\n ------------ ', datapath)
        print()

        dataname = 'result/{}-{}-{}-{}-{}.csv'.format(strategy, sep[0], start.replace('-',''), end.replace('-',''), sep[3])
        csvfile = open(dataname, 'w', newline='')
        result_writer = csv.writer(csvfile, delimiter=',')

        result_writer.writerow(['Pair', 'Timeframe', 'Start', 'End', 'Strategy', 'Period', 'Final value', '%', 'Total win', 'Total loss', 'SQN']) # init header


        for period in periodRange:
            end_val, totalwin, totalloss, pnl_net, sqn = runbacktest(datapath, start, end, period, strategy, commission_val, portofolio, stake_val, quantity, plot)
            profit = (pnl_net / portofolio) * 100

            # view the data in the console while processing
            print('data processed: %s, %s (Period %d) --- Ending Value: %.2f --- Total win/loss %d/%d, SQN %.2f' % (datapath[5:], strategy, period, end_val, totalwin, totalloss, sqn))

            result_writer.writerow([sep[0], sep[3] , start, end, strategy, period, round(end_val,3), round(profit,3), totalwin, totalloss, sqn])

        csvfile.close()
        
async def gather_strategy_coros(strategies, symbol, periodRange, start, end, timeframe) -> None:
    coros = [run_strategy(strategy, symbol, periodRange, start, end, timeframe) for strategy in strategies]
    await asyncio.gather(*coros)


# MAIN ENTRYPOINT
if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    commission_val = 0.04 # 0.04% taker fees binance usdt futures
    portofolio = 10000.0 # amount of money we start with
    stake_val = 1
    quantity = 0.10 # percentage to buy based on the current portofolio amount
    # here it would be a unit equivalent to 1000$ if the value of our portofolio didn't change

    start = '2020-12-30'
    end = '2021-12-31'
    timeframe = '1d'
    # strategies = ['SMA', 'RSI']
    strategies = ['RSI']
    periodRange = range(14, 15)
    plot = False
    symbol = "BTCUSDT"

    loop.run_until_complete(gather_strategy_coros(strategies, symbol, periodRange, start, end, timeframe))