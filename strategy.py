# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 18:13:50 2018

@author: blins
"""

from abc import ABCMeta, abstractmethod
from event import SignalEvent
from queue import *

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import math
import copy

from sizer import EqualPercentageSizer

class Strategy(object):
    
    @abstractmethod
    def get_signals(self, event):
        pass

    def log_vars(self):
        pass
    
    def initial_code(self):
        pass
    
    def set_params(self, bars, events, portfolio):
        self.bars = bars
        self.symbols = bars.symbols
        self.events = events
        self.portfolio = portfolio
        
    def send(self,symbol,direction,quantity = None):
        signal = SignalEvent(symbol,self.bars.bar_back(symbol,0)[1],direction,quantity = quantity)
        self.events.put(signal)
        
    def order(self, symbol, shares):
        signal = SignalEvent(symbol, amount=shares, amount_type='SHARES', target=False)
        self.events.put(signal)
    
    def order_target(self, symbol, shares):
        signal = SignalEvent(symbol, amount=shares, amount_type='SHARES', target=True)
        self.events.put(signal)
    
    def order_value(self, symbol, value):
        signal = SignalEvent(symbol, amount=value, amount_type='VALUE', target=False)
        self.events.put(signal)
    
    def order_target_value(self, symbol, value):
        signal = SignalEvent(symbol, amount=value, amount_type='VALUE', target=True)
        self.events.put(signal)
    
    def order_percent(self, symbol, percentage):
        signal = SignalEvent(symbol, amount=percentage, amount_type='PERCENTAGE', target=False)
        self.events.put(signal)
        
    def order_target_percent(self,symbol,percentage):
        signal = SignalEvent(symbol, amount=percentage, amount_type='PERCENTAGE', target=True)
        self.events.put(signal)
        
    def schedule_function(self,  
                          func_to_run,
                          interval,
                          offset):
        pass
        
class TestStrategy(Strategy):
    
    def __init__(self):
        pass
    
    def get_signals(self, event):
        if self.bars.data_length > 2:
            for s in self.symbols:
                if self.bars.bar_back(s,0)[5] > self.bars.bar_back(s,-1)[5]:
                    self.send(s,'LONG')
                    

class Momentum(Strategy):
     
    def __init__(self):
        self.look_back = 50
        self.number_held = 20 #number of stocks to hold
        self.ranked_stocks = pd.DataFrame()
        self.percentage = 1.00/self.number_held
        
    def setup(self):
        self.sizer = EqualPercentageSizer(self.portfolio,self,self.bars,0.05)
        pass
    
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
        
        
    
class BuyHold(Strategy):
    
    def __init__(self):
        self.bought = False
        self.aapl = 'AAPL'
        self.target_leverage = 1.00
        self.target_stocks = ['AAPL','MSFT','GS','AMZN','FB']
        self.num_stocks = 5
        
    def setup(self):
        self.bought = False
        
    def get_signals(self, event):
        """
        for s in self.symbols:
            if not math.isnan(self.bars.bar_back(s,0)[2]):
                if self.bought[s] is False:
                    self.send(s,'LONG')
                    self.bought[s] = True
            
        """
        percent = self.target_leverage / self.num_stocks
        
        if self.bought is False:
            for stock in self.target_stocks:
                self.order_target_percent(stock, percent)
            self.bought = True
            
            
            
            
            
            
            
            
        