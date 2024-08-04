# SMA(Simple Moving Average) Crossover Strategy 

## Project Overview
This project aims to bridge the gap between backtesting and live trading by integrating a simple daily trading strategy developed using Backtrader with Interactive Brokers' paper trading account. This will allow real-time testing of the strategy's performance in a simulated market environment.

## Mission
To implement, connect, and test a daily trading strategy using Backtrader with Interactive Brokers' paper trading account.

## Setup Instructions
1. Sign up for an Interactive Brokers (IB) Account
   * Set up a paper trading account for simulated trading.
2. Install Backtrader and IB API Wrapper(‘ib_insync’).
   * Install Backtrader: 
     ```python
     pip install backtrader
     ```
   * Install ib_insync:
     ```python
     pip install ib_insync
     ```
3. Install TWS(Trader Workstation) or IB Gateway
   * Download [TWS](https://www.interactivebrokers.com/en/trading/tws.php#tws-software)
   * Download [IB Gateway](https://www.interactivebrokers.com/en/trading/ibgateway-stable.php)
4. Configure TWS/IB Gateway for API Access
   * Launch TWS/IB Gateway and log in with IB paper trading account.
   * Go to Configure on the top right of the screen.
   * Under API > Settings, ensure the following options are set:
     * Enable ActiveX and Socket Clients: *Checked*
     * Read-Only API: *Unchecked*
     * Socket port: Default is **7497** for paper trading

## Integration of Backtrader with IB API
Example code for connecting to IB:<br>
```python
from ib_insync import IB

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)    # Default paper trading port is 7497
```

## Running the Strategy
* Historical Data Backtest Strategy
  ```python
  python HistoricalDataStrategy.py
  ```
* Real-time Backtest strategy
  ```python
  python RealTimeStrategy.py
  ```

