
from solitude.trader import Trader
from test_strategy import TestStrategy
import datetime as dt
from solitude.commission import IBCommission
from solitude.datafeed import CDFDataFeed, CSVDataFeed
from solitude.strategy import Strategy
import os
import pandas as pd

class TestStrategy(Strategy):

    def setup(self):
        self.symbol = 'AAPL'

    def log_vars(self):
        pass

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

        
        

if __name__ == '__main__':

    """
    path = os.path.dirname(os.path.realpath(__file__))
    subdirs = next(os.walk(path))[1]
    idx = subdirs.index('data')
    data_path = os.path.join(path, subdirs[idx])
    file = pd.read_csv('tickers.txt', sep=',')
    symbols = set(file['Symbol'].tolist())
    data = CSVDataFeed(data_path, symbols)
    """


    trader = Trader(
        CDFDataFeed('stock_data.nc'),
        TestStrategy()
        )

    trader.set_run_settings(
        cash = 100000,
        log_orders = False,
        start = dt.date(2005, 1, 1),
        end = dt.date(2018, 1, 30),
        commission = IBCommission()
        )
        
    trader.run()
    trader.results()