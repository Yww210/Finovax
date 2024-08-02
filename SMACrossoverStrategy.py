from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os.path
import datetime

# Import the backtrader platform
import backtrader as bt

# Create a Stratey
class SMACrossover(bt.Strategy):
    params = (
        ('short_period', 10),
        ('long_period', 30),
    )

    def __init__(self):
        self.short_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.short_period)   # short-term moving average 
        self.long_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.long_period)    # long-term moving average
        self.crossover = bt.indicators.CrossOver(self.short_ma, self.long_ma)

    def next(self):
        if not self.position:
            if self.crossover > 0:  # short_ma crosses above long_ma
                self.buy()
        elif self.crossover < 0:  # short_ma crosses below long_ma
            self.sell()

if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(SMACrossover)

    # Get historical data from CSV
    data_path = os.path.join(os.getcwd(), 'AAPL.csv')

    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=data_path,
        fromdate=datetime.datetime(2023, 1, 1),
        todate=datetime.datetime(2024, 1, 1),
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.set_cash(10000)

    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()
