from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime
from typing import List  # For datetime objects
import backtrader as bt # Import the backtrader platform#
import csv, os, asyncio, time
from random import random

class RSIDivergence(bt.ind.PeriodN):
    lines = ('signal',)
    params = dict(
        rsi_period=30,
        hl_period=100,
        hl_min=25
    )

    def __init__(self):
        self.hfi = bt.ind.FindFirstIndexHighest(self.data.high, period=self.p.hl_period)
        self.lfi = bt.ind.FindFirstIndexLowest(self.data.low, period=self.p.hl_period)
        self.rsi = bt.ind.RSI_Safe(period=self.p.rsi_period)

    def signal_get(self):
        signal = 0
        if self.hfp >= self.hsp:
            if self.rsi[-int(self.hfi[0])] < self.rsi[-int(self.hsi)]:
                signal -= 1

        if self.lfp <= self.lsp:
            if self.rsi[-int(self.lfi[0])] > self.rsi[-int(self.lsi)]:
                signal += 1

        return signal

    def next(self):
        h_iterable = self.data.get(size=self.p.hl_period, ago=-int(self.hfi[0]) - self.p.hl_min)
        l_iterable = self.data.get(size=self.p.hl_period, ago=-int(self.lfi[0]) - self.p.hl_min)

        if len(h_iterable) > 0 and len(l_iterable) > 0:
            m = max(h_iterable)
            self.hsi = next(i for i, v in enumerate(reversed(h_iterable)) if v == m) + int(self.hfi[0]) + self.p.hl_min

            m = min(l_iterable)
            self.lsi = next(i for i, v in enumerate(reversed(l_iterable)) if v == m) + int(self.lfi[0]) + self.p.hl_min

            self.hfp = self.data.high[-int(self.hfi[0])]
            self.hsp = self.data.high[-int(self.hsi)]
            self.lfp = self.data.low[-int(self.lfi[0])]
            self.lsp = self.data.low[-int(self.lsi)]

            self.lines.signal[0] = self.signal_get()
        else:
            self.lines.signal[0] = 0
class BOLLStrat(bt.Strategy):
 
    '''
    This is a simple mean reversion bollinger band strategy.
 
    Entry Critria:
        - Long:
            - Price closes below the lower band
            - Stop Order entry when price crosses back above the lower band
        - Short:
            - Price closes above the upper band
            - Stop order entry when price crosses back below the upper band
    Exit Critria
        - Long/Short: Price touching the median line
    '''
 
    params = (
        ("period", 10),
        ("devfactor", 2),
        ("size", 100),
        ("debug", False)
        )
 
    def __init__(self):
        self.boll = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        #self.sx = bt.indicators.CrossDown(self.data.close, self.boll.lines.top)
        #self.lx = bt.indicators.CrossUp(self.data.close, self.boll.lines.bot)
 
    def next(self):
 
        orders = self.broker.get_orders_open()
 
        # Cancel open orders so we can track the median line
        if orders:
            for order in orders:
                self.broker.cancel(order)
 
        if not self.position:
 
            if self.data.close > self.boll.lines.top:
 
                self.sell(exectype=bt.Order.Stop, price=self.boll.lines.top[0], size=self.p.size)
 
            if self.data.close < self.boll.lines.bot:
                self.buy(exectype=bt.Order.Stop, price=self.boll.lines.bot[0], size=self.p.size)
 
 
        else:
 
 
            if self.position.size > 0:
                self.sell(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)
 
            else:
                self.buy(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)
 
        if self.p.debug:
            print('---------------------------- NEXT ----------------------------------')
            print("1: Data Name:                            {}".format(data._name))
            print("2: Bar Num:                              {}".format(len(data)))
            print("3: Current date:                         {}".format(data.datetime.datetime()))
            print('4: Open:                                 {}'.format(data.open[0]))
            print('5: High:                                 {}'.format(data.high[0]))
            print('6: Low:                                  {}'.format(data.low[0]))
            print('7: Close:                                {}'.format(data.close[0]))
            print('8: Volume:                               {}'.format(data.volume[0]))
            print('9: Position Size:                       {}'.format(self.position.size))
            print('--------------------------------------------------------------------')
 
    def notify_trade(self,trade):
        if trade.isclosed:
            dt = self.data.datetime.date()
 
            # print('---------------------------- TRADE ---------------------------------')
            # print("1: Data Name:                            {}".format(trade.data._name))
            # print("2: Bar Num:                              {}".format(len(trade.data)))
            # print("3: Current date:                         {}".format(dt))
            # print('4: Status:                               Trade Complete')
            # print('5: Ref:                                  {}'.format(trade.ref))
            # print('6: PnL:                                  {}'.format(round(trade.pnl,2)))
            # print('--------------------------------------------------------------------')

class RSIStrategy(bt.Strategy):
    params = (
        ('verbose', False),
        ('maperiod', None),
        ('quantity', None),
        ('stopLoss', 0.00),
        ('limits', None),
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
        # self.rsi = bt.talib.RSI(self.datas[0], timeperiod=self.params.maperiod)
        self.rsi = bt.indicators.RelativeStrengthIndex()
        self.movav= bt.talib.MACD(self.datas[0], timeperiod=self.params.maperiod)
        self.order_stopLoss = None
        self.rsiDivergence = RSIDivergence(rsi_period=self.params.maperiod)

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

                if self.params.verbose:
                    print('BOUGHT @price: {:.2f} {}'.format(order.executed.price, bt.num2date(order.executed.dt)))
                if self.params.stopLoss:
                    if self.params.stopLoss > 0:
                        stop_price = order.executed.price * (1 - self.params.stopLoss)
                        self.order_stopLoss = self.sell(exectype=bt.Order.Stop, price=stop_price)
                        if self.params.verbose:
                            print('  STOP @price: {:.2f}'.format(stop_price))
                    else:
                        # trailing stop specified % under executed price
                        self.order_stopLoss = self.sell(exectype=bt.Order.StopTrail, trailpercent=0-self.params.stopLoss)
                        self.order_stopLoss.addinfo(ordername="STOPLONG")
                        if self.params.verbose:
                            print('  STOP TRAILING')

            else:
                if not self.position:  # we left the market
                    self.broker.cancel(self.order_stopLoss)
                    self.order_stopLoss = None
                    if self.params.verbose:
                        print('SOLD @price: {:.2f} cost: {:.2f} comm: {:.2f} {}'.format(order.executed.price, order.executed.value, order.executed.comm, bt.num2date(order.executed.dt)))

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        if self.params.verbose:
            print('PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))
            print('_______________________________________________')


    def next(self):
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return
        # Check if we are in the market
        if not self.position:
            # Not yet ... we MIGHT BUY if ...
            if self.rsi < min(self.params.limits):
                # Keep track of the created order to avoid a 2nd order
                self.amount = (self.broker.getvalue() * self.params.quantity) / self.dataclose[0]
                self.order = self.buy(size=self.amount)
        else:
            # Already in the market ... we might sell
            if self.rsi > max(self.params.limits):
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
    
def runbacktest(verbose, datapath, start, end, period, strategy, commission_val=None, portofolio=10000.0, stake_val=1, quantity=0.01, plt=True, limits=[30, 70], stopLoss=0.0,):
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=stake_val) # Multiply the stake by X
    cerebro.broker.setcash(portofolio) # default : 10000.0
    
    if commission_val:
        cerebro.broker.setcommission(commission=commission_val/100) # divide by 100 to remove the %
    # Add a strategy
    if strategy == 'RSI':
        # cerebro.optstrategy(RSIStrategy, maperiod=period, quantity=quantity)
        cerebro.addstrategy(RSIStrategy, verbose=verbose, maperiod=period, quantity=quantity, stopLoss=stopLoss, limits=limits)
    elif strategy == 'BOLLStrat':
        cerebro.addstrategy(BOLLStrat)
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
        fromdate = datetime.strptime(start, '%Y-%m-%d'),
        todate = datetime.strptime(end, '%Y-%m-%d'),
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


# async def run_strategy_and_write_results_to_file(strategy: str, periodRange: List[int], stopLossRange: List[float], limitsRange: List[int], start, end):
#     # time.sleep(20)

#     for data in os.listdir("./data"):
#     # for i, data in enumerate(os.listdir("./data")):
#         print('IN loop....')
#         # if i == 0:
#             # data = os.listdir("./data")

#         datapath = 'data/' + data
#         sep = datapath[5:-4].split(sep='-') # ignore name file 'data/' and '.csv'

#         dataname = f"result/{strategy}-{sep[0]}-{start.replace('-','')}-{end.replace('-','')}-{sep[3]}.csv"
#         csvfile = open(dataname, 'w', newline='')
#         result_writer = csv.writer(csvfile, delimiter=',')
#         result_writer.writerow(['Pair', 'Timeframe', 'Start', 'End', 'Strategy', 'Period', 'Final value', '%', 'Total win', 'Total loss', 'SQN']) # init header

#         for period in periodRange:
#             for limits in limitsRange:
#                 for stopLoss in stopLossRange:
#                     end_val, totalwin, totalloss, sqn, profit = run_strategy(strategy, start, end, datapath, period, limits, stopLoss)
#                     result_writer.writerow([sep[0], sep[3] , start, end, strategy, period, round(end_val,3), round(profit,3), totalwin, totalloss, sqn])
#         csvfile.close()

def run_strategy(strategy, datapath, start, end,  period, limits, stopLoss, verbose):
    end_val, totalwin, totalloss, pnl_net, sqn = runbacktest(verbose, datapath, start, end, period, strategy, commission_val, portofolio, stake_val, quantity, plot, limits, stopLoss)
    profit = (pnl_net / portofolio) * 100
                    # view the data in the console while processing
                    # print('data processed: %s, %s (Period %d, limits %d, stopLoss %d,) --- Ending Value: %.2f --- Total win/loss %d/%d, SQN %.2f' % (datapath[5:], strategy, period, end_val, totalwin, totalloss, sqn))
    print(f"data processed: {datapath[5:]}, {strategy} (period {period}, limits {limits}, stopLoss {stopLoss}) --- Ending Value: {end_val} --- Total win/loss {totalwin}/{totalloss}, {sqn}")
    return end_val,totalwin,totalloss,sqn,profit

# async def gather_strategy_coros(strategies, periodRange, stopLossRange, limitsRange, start, end) -> None:
#     coros = [run_strategy(strategy, periodRange, stopLossRange, limitsRange, start, end) for strategy in strategies]
#     await asyncio.gather(*coros)


# MAIN ENTRYPOINT
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    commission_val = 0.04 # 0.04% taker fees binance usdt futures
    portofolio = 1000.0 # amount of money we start with
    stake_val = 1
    quantity = 0.01 # percentage to buy based on the current portofolio amount
    # here it would be a unit equivalent to 1000$ if the value of our portofolio didn't change

    periodRange = range(15, 16)
    # periodRange = range(10, 30)
    # stopLossRange = [0, 0.001, 0.005, 0.01, -0.01]
    stopLossRange = [0]
    # limitsRange = [[70,30], [70,25], [60,25], [65,25], [70,20]]
    limitsRange = [[60,25], [65,25], [65,30], [70,25], [70,30], [75,30], [75,25], [80,25], [80,30], [80,35], [80,40]]
    # limitsRange = [[65,25]]
    start = '2020-01-01'
    end = '2022-01-29'
    # timeframe = '1d'
    # strategies = ['SMA', 'RSI']
    strategies = ['RSI']
    # strategies = ['BOLLStrat']
    # strategies = ['firstStrategy']
    plot = True
    # symbol = "BTCUSDT"
    import multiprocessing
    import time
    
    def get_params():
        paramsIterations = []
        for strategy in strategies:
            for period in periodRange:
                for stopLoss in stopLossRange:
                    for limits in limitsRange:
                        # datapath = 'data/' + os.listdir("./data")[0]
                        datapath = "data/XRPUSDT-20170101-20220129-30m.csv"
                        sep = datapath[5:-4].split(sep='-') # ignore name file 'data/' and '.csv'

                        dataname = f"result/{strategy}-{sep[0]}-{start.replace('-','')}-{end.replace('-','')}-{sep[3]}.csv"
                        params = (strategy, datapath, start, end, period, limits, stopLoss, False)
                        paramsIterations.append(params)
                        # yield params
        return paramsIterations

    print(get_params())
    tic = time.time()
    print(f"# CPUs: {multiprocessing.cpu_count()}")
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    # Params: strategy, datapath, start, end, period, limits, stopLoss, verbose
    # pool.map(run_strategy, get_params())
    pool.starmap(run_strategy, get_params())
    # pool.starmap(run_strategy, [('RSI', 'data/DOGEUSDT-20170101-20220129-30m.csv', '2017-01-01', '2022-01-29', 14, [70, 20], 0)])
    # pool.close()

    # loop.run_until_complete(gather_strategy_coros(strategies, periodRange, stopLossRange, limitsRange, start, end))