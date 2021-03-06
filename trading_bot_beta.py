# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 00:07:37 2018

@author: blins
"""

from solitude.trader import Trader
from solitude.datafeed import CSVDataFeed
from solitude.commission import IBCommission
from example_strategies import BuyHold, TestSchedule
from test_strategy import TestStrategy
#from solitude.mom_strategy import MomentumStrat

import pandas as pd
import datetime as dt
import os

if __name__ == '__main__':
    
    #strategy_list = {0: BuyHold(), 
    #                 1: MomentumStrat(),
    #                 2: TestSchedule()}
    
    path = os.path.dirname(os.path.realpath(__file__))
    subdirs = next(os.walk(path))[1]
    
    try:
        idx = subdirs.index('data')
        data_path = os.path.join(path, subdirs[idx])

        trader = Trader()
    
        file = pd.read_csv('tickers.txt', sep=',')
        symbols = set(file['Symbol'].tolist())
        """
        symbols = set()
        for row in file.itertuples():
            symbols.add(row[1])
        """
        data = CSVDataFeed(data_path, trader.events, symbols)
        
        trader.add_data(data)
        trader.set_strategy(TestStrategy())
        trader.set_run_settings(cash = 50000,
                                log_orders = False,
                                start = dt.date(2005, 1, 1),
                                end = dt.date(2005, 1, 30),
                                commission = IBCommission()
                                )
        
        trader.run()

        trader.results()
        
    except ValueError:
        print('Error: data subfolder not found')
    
    
    
    
    
    
    