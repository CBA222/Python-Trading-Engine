# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 02:26:05 2018

@author: blins
"""
from strategy import Strategy
from utils.schedulerule import every_month
import datetime as dt

class MomentumStrat(Strategy):
    
    def __init__(self):
        self.security_list = []
        self.target_stocks = 20
        self.target_leverage = 1.00
        self.lookback = 90
        
        self.time_passed = 0
        
    
    def setup(self):
        self.set_start_date(dt.date(2003, 10, 1))
        self.set_end_date(dt.date(2018, 1, 1))
        
        self.elapsed = 0
        self.frequency = 20
        
        self.security_list = list(self.bars.symbols)
        
        self.schedule_function(self.rebalance,
                               every_month())
        
    def get_signals(self, event):
        
        if event.type != 'MARKET':
            return
        
        self.time_passed += 1
        
    def rebalance(self):

        if self.time_passed < self.lookback:
            return
        
        hist = self.bars.history(self.security_list, 
                                    fields = 'close', 
                                    bar_count=self.lookback, 
                                    convert_to_pandas = True)
        hist = hist.T
        mom = (hist.iloc[-1] - hist.iloc[0]) / hist.iloc[0]
        self.long_list = mom.sort_values(ascending=False).iloc[0:self.target_stocks]
        
        percent = self.target_leverage / self.target_stocks
        
        #num_to_buy = self.target_stocks - len(self.portfolio.open_positions())
        
        for stock in self.long_list.index:
            if stock not in self.portfolio.open_positions().index:
                self.order_target_percent(stock, percent)
                #print('star', stock, percent, self.portfolio.calculate_total_value())
            
        for stock in self.portfolio.open_positions().index:
            if stock not in self.long_list.index:
                self.order_target_percent(stock, 0)
                #print('star', stock, 0, self.portfolio.calculate_total_value())
        
        #print(self.portfolio.open_positions())        
        #print('')
                
    
    def log_vars(self):
        #print(len(self.portfolio.positions))
        pass
        