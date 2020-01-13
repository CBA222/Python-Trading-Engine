# Solitude: A Trading Engine in Python

Solitude is a stock trading engine written in Python.

Solitude allows you to perform backtests with historical stock data on custom trading strategies.

## Installation

    pip install solitude

## Usage

### Example
```python
from solitude.trader import Trader
from solitude.datafeed import CDFDatafeed
import datetime as dt

class TestStrategy(Strategy):

    def setup(self):
        self.symbol = 'AAPL'

    def get_signals(self, event):
        try:
            history_10d = self.bars.history(self.symbol, 'adj_close', 10)
            returns_10d = history_10d.iloc[-1] / history_10d.iloc[0]

            if returns_10d > 0.0:
                self.order_target_percent(self.symbol, 0.5)
            else:
                self.order_target_percent(self.symbol, 0.0)
        except ValueError:
            return

trader = Trader(
    CDFDataFeed('stock_data.nc'), 
    TestStrategy()
    )

trader.set_run_settings(
    cash = 100000,
    log_orders = False,
    start = dt.date(2005, 1, 1),
    end = dt.date(2005, 1, 30),
    commission = IBCommission()
    )
    
trader.run()
trader.results()
```

First, you must implement the Strategy class defined in strategy.py (as a subclass) and put this in a seperate file. Examples can be found in the examples folder. 

### Basic Example
    solitude -st buy_hold.py -sd 01-01-2014 -ed 05-20-2016

This will run a backtest using the strategy defined in buy_hold.py from January 1st, 2014 to May 20th, 2016.

### Additional Options

The choice of starting cash and what commission to use during the backtest are also customizable using the -ch and -cm flags respectively. 

For example:

    solitude -st strategy.py -sd 01-01-2014 -ed 05-20-2016 -cm IB -ch 500



