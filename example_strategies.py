# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 03:01:12 2018

@author: blins
"""
from strategy import Strategy
from sizer import EqualPercentageSizer
from utils.schedulerule import every_month, every_week, n_months

import pandas as pd
import datetime as dt
import copy

class TestSchedule(Strategy):
    
    def __init__(self):
        pass
    
    def setup(self):
        self.set_start_date(dt.date(2015, 12, 1))
        self.set_end_date(dt.date(2018, 3, 1))
        self.schedule_function(self.rebalance,
                               n_months(offset = 0, N = 1))
        
    def rebalance(self):
        print('rebalance', self.bars.current_date())
        
    def get_signals(self, event):
        #print('get_signals', self.bars.current_date())
        pass
    
    def log_vars(self):
        pass

class TestStrategy(Strategy):
    
    def __init__(self):
        pass
    
    def get_signals(self, event):
        if self.bars.data_length > 2:
            for s in self.symbols:
                if self.bars.bar_back(s,0)[5] > self.bars.bar_back(s,-1)[5]:
                    self.send(s,'LONG')

class BuyHold(Strategy):
    
    def __init__(self):
        self.bought = False
        self.aapl = 'AAPL'
        self.target_leverage = 1.00
        self.target_stocks = ['AAPL','MSFT','GS','AMZN','FB']
        self.num_stocks = 5
        
    def setup(self):
        self.bought = False
        self.set_start_date(dt.date(2015, 12, 1))
        self.set_end_date(dt.date(2018, 3, 1))
    
    def log_vars(self):
        pass
        
    def get_signals(self, event):
        percent = self.target_leverage / self.num_stocks
        
        if self.bought is False:
            for stock in self.target_stocks:
                self.order_target_percent(stock, percent)
            self.bought = True

class Momentum(Strategy):
     
    def __init__(self):
        pass
        
    def setup(self):
        self.sizer = EqualPercentageSizer(self.portfolio,self,self.bars,0.05)
        self.look_back = 50
        self.number_held = 20 #number of stocks to hold
        self.ranked_stocks = pd.DataFrame()
        self.percentage = 1.00/self.number_held
    
    def get_signals(self, event):
        if self.bars.data_length is self.look_back+1:
            self.initial_allocation()
            
        elif self.bars.data_length > self.look_back+1:
            self.rank_stocks()
            for s in self.portfolio.current_holdings:
                if s in self.fallen_out:
                    if self.portfolio.current_holdings[s]['Quantity'] > 0:
                       #self.send(s,'SHORT',self.portfolio.current_holdings[s]['Quantity'])
                       self.order_target_percent(s,0)
                    
            for s in self.ranked_stocks:
                if s in self.portfolio.current_holdings:
                    if self.portfolio.current_holdings[s]['Quantity'] is 0:
                       #self.send(s,'LONG',self.sizer.return_size(s))
                       self.order_target_percent(s,self.percentage)
        
    def initial_allocation(self):
       temp_list = []
       for s in self.symbols:
           temp_list.append([s,self.bars.bar_back(s,0)[5] - self.bars.sma(s,self.look_back)])
       self.ranked_stocks = pd.DataFrame(temp_list).sort_values(1,ascending=False)
       self.ranked_stocks = self.ranked_stocks.iloc[0:self.number_held,0]
       
       for i in range(0,self.number_held):
           symbol = self.ranked_stocks.iloc[i]
           #self.send(symbol,'LONG',self.sizer.return_size(symbol))
           self.order_target_percent(symbol,self.percentage)
        
    def rank_stocks(self):
        self.old_ranked = copy.deepcopy(self.ranked_stocks)
        temp_list = []
        for s in self.symbols:
            temp_list.append([s,self.bars.bar_back(s,0)[5] - self.bars.sma(s,self.look_back)])
        self.ranked_stocks = pd.DataFrame(temp_list).sort_values(1,ascending=False)
        self.ranked_stocks = self.ranked_stocks.iloc[0:self.number_held,0]
        
        self.fallen_out = []
        for i in range(0,self.number_held):
            if self.old_ranked.iloc[i] not in self.ranked_stocks:
                self.fallen_out.append(self.old_ranked.iloc[i])
        
        
    

            
            
            
            
            
            
            
            
        