# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 00:07:37 2018

@author: blins
"""

from trader import Trader
from datafeed import CSVDataFeed
from example_strategies import BuyHold, TestSchedule
import pandas as pd
from mom_strategy import MomentumStrat

import os

if __name__ == '__main__':
    
    strategy_list = {0: BuyHold(), 
                     1: MomentumStrat(),
                     2: TestSchedule()}
    
    path = os.path.dirname(os.path.realpath(__file__))
    subdirs = next(os.walk(path))[1]
    
    try:
        idx = subdirs.index('data')
        data_path = os.path.join(path, subdirs[idx])

        trader = Trader()
    
        file = pd.read_csv('tickers.txt', sep=',')
        symbols = set()
        for row in file.itertuples():
            symbols.add(row[1])
        
        data = CSVDataFeed(data_path, trader.events, symbols)
        
        trader.add_data(data)
        trader.add_strategy(strategy_list[1])
        trader.set_starting_cash(50000)
        trader.set_run_settings(log_orders = False)
        
        trader.run()
        
    except ValueError:
        print('Error: data subfolder not found')
    
    
    
    
    
    
    