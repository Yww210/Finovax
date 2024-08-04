from ib_insync import *
import backtrader as bt
import pandas as pd

class SMACrossover(bt.Strategy):
    params = (
        ('short_period', 20),
        ('long_period', 50),
    )

    def __init__(self):
        self.short_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.short_period)
        self.long_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.long_period)
        self.crossover = bt.indicators.CrossOver(self.short_ma, self.long_ma)
        self.ib = None

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
                self.place_order('BUY')
        elif self.crossover < 0:
            self.sell()
            self.place_order('SELL')

    def start(self):
        self.ib = IB()
        self.ib.connect('127.0.0.1', 7497, clientId=1)
        self.contract = Stock('AAPL', 'SMART', 'USD')
        self.ib.qualifyContracts(self.contract)
        
    def place_order(self, action):
        order = MarketOrder(action, 10)
        trade = self.ib.placeOrder(self.contract, order)
        self.ib.sleep(1)

    def stop(self):
        self.ib.disconnect()

if __name__ == '__main__':
    # IB connection
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=2)

    # Define contract
    contract = Stock('AAPL', 'SMART', 'USD')
    ib.qualifyContracts(contract)

    # Request historical data
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='30 D',
        barSizeSetting='1 min',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1,
        keepUpToDate=True
    )

    # Convert data format
    df = util.df(bars)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    data = bt.feeds.PandasData(dataname=df)

    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add the strategy
    cerebro.addstrategy(SMACrossover)

    # Add the data feed to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.set_cash(10000)

    # Set commission
    cerebro.broker.setcommission(commission=0.001)

    # Add sizer
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run strategy
    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Disconnect IB connection
    ib.disconnect()
