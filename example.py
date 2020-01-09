
from solitude.trader import Trader
from test_strategy import TestStrategy
import datetime as dt
from solitude.commission import IBCommission
from solitude.datafeed import CDFDataFeed, GenericDataFeed
import os
import pandas as pd

if __name__ == '__main__':

    """
    path = os.path.dirname(os.path.realpath(__file__))
    subdirs = next(os.walk(path))[1]
    idx = subdirs.index('data')
    data_path = os.path.join(path, subdirs[idx])
    file = pd.read_csv('tickers.txt', sep=',')
    symbols = set(file['Symbol'].tolist())
    data = GenericDataFeed(data_path, symbols)
    """

    data = CDFDataFeed('stock_data.nc')
    trader = Trader(data, TestStrategy())

    trader.set_run_settings(
        cash = 50000,
        log_orders = False,
        start = dt.date(2005, 1, 1),
        end = dt.date(2005, 1, 30),
        commission = IBCommission()
        )
        
    trader.run()
    trader.results()