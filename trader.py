# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 21:53:53 2018

@author: blins
"""

#import Queue

from orderhandler import SimpleOrderHandler

from queue import *

class Trader(object):
    """
    class managing event driven loop
    """
    
    def __init__(self):
        self.events = Queue()
        #self.broker = SimpleOrderHandler()
    
    def add_data(self, data):
        self.data = data
        
    def add_strategy(self, strat):
        self.strategy = strat
        
    def set_commission(self, commission):
        self.commission = commission
        
    def set_portfolio(self, portfolio):
        self.portfolio = portfolio
        
    def run(self):
        #setup
        print("Initialized")
        self.portfolio.set_params(self.events,self.data)
        self.strategy.set_params(self.data,self.events, self.portfolio)
        self.broker = SimpleOrderHandler(self.events,self.data)
        self.portfolio.setup()
        self.strategy.setup()
        
        while True:
            if self.data.keep_iterating == True:
                self.data.update()
            else:
                break
            
            while True:
                if self.events.empty():
                    break
                else:
                    event = self.events.get()
                    
                if event.type == 'MARKET':
                    self.strategy.get_signals(event)
                    self.broker.execute_pending(event)
                    
                if event.type == 'SIGNAL':
                    self.portfolio.update_orders(event)
                    
                if event.type == 'ORDER':
                    self.broker.send_order(event)
                    
                if event.type == 'FILL':
                    self.portfolio.update_fill(event)
                
            #self.broker.execute_pending()
            self.portfolio.update_holdings()
            self.strategy.log_vars()
                
                    
                    
                    
                    
                    
                    
                    