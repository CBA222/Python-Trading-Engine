# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 00:07:37 2018

@author: blins
"""

from trader import Trader
from datafeed import DataFeed, CSVDataFeed
from strategy import TestStrategy,Momentum,BuyHold
from portfolio import DumbPortfolio
import pandas as pd

import os

if __name__ == '__main__':
    
    trader = Trader()
    
    file = pd.read_csv('tickers.txt', sep=',')
    symbols = set()
    for row in file.itertuples():
        symbols.add(row[1])
    
    #path = os.getcwd()
    path = 'C:\\Users\\blins\\Documents\\Projects\\Custom Backtest Engine\\data'
    data = CSVDataFeed(path, trader.events, symbols)
    
    trader.add_data(data)
    trader.add_strategy(BuyHold())
    trader.set_portfolio(DumbPortfolio(10000))
    
    trader.set_commission(5)
    
    trader.run()
    
    print('Final Portfolio Value: %s' % trader.portfolio.calculate_portfolio_value())
    print('Final Cash Value: %s' % trader.portfolio.current_cash)
    total = trader.portfolio.calculate_portfolio_value() + trader.portfolio.current_cash
    print("Total Value: ",total)
    print("Absolute Return: " , ((total/10000)*100)-100, '%')
    
    
    
    