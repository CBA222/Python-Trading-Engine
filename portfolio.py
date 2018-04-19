# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 21:45:43 2018

@author: blins
"""

import copy
from orderhandler import OrderEvent
import math

class Portfolio:
    
    def update_orders(self, event):
        """
        Sends out orders based on signal events from Strategy objects
        """
        pass
    
    def update_fill(self, event):
        """
        Updates portfolio as orders are filled by the broker
        """
        pass
    
    def set_params(self, events, bars):
        self.bars = bars
        self.events = events
        
    class Position:
        
        def __init__(self, symbol, shares, price_paid):
            self.symbol = symbol
            self.shares = shares
            self.price_paid = price_paid
            self.open = True
            self.price = price_paid / shares
            
        def update(self, price):
            self.price = price
    
class DumbPortfolio(Portfolio):
    
    def __init__(self, starting_capital):
        """
        all_holdings is a list holding nested dictionaries
        Each list element represents one unit of time, inside it is a dictionary
        listing the current holdings of each symbol, as well as the current cash
        
        current_holdings hold the most recent dictionary
        
        """
        
        self.all_holdings = []
        self.current_holdings = {}
        self.all_cash = []
        self.current_cash = 0
        self.starting_capital = starting_capital
        self.default_quantity = 1
        #self.cash = cash
        
        
    def setup(self):
        #create initial holdings
        self.all_holdings.append({})
        
        for s in self.bars.symbols:
            self.all_holdings[-1][s] = {'DateTime':None,'Quantity':0,'Price':0}
            self.current_holdings[s] = {'DateTime':None,'Quantity':0,'Price':0}
            
        self.all_cash.append(self.starting_capital)
        self.current_cash = self.starting_capital
        
        
    def update_holdings(self):
        """
        Updates the prices for the Portfolio's holdings according to current market close
        
        all_holdings contains all previos holdings + current_holdings
        
        This function creates a new current_holding based on current prices and appends it to all_holdings
        """
        
        new_holdings = copy.deepcopy(self.current_holdings)
        
        for symbol,cost in new_holdings.items():
            new_holdings[symbol]['Price'] = self.bars.current(symbol, 'adj_close').item()
            new_holdings[symbol]['DateTime'] = ""
            
        self.current_holdings = new_holdings
        self.all_holdings.append(self.current_holdings)
        self.all_cash.append(self.current_cash)
        
    def update_fill(self, event):
        if event.type is 'FILL':
            dir = 0
            if event.direction is 'LONG':
                dir = 1
            elif event.direction is 'SHORT':
                dir = -1
            
            self.current_holdings[event.symbol]['Quantity'] += event.quantity*dir 
            self.current_cash -= event.value*dir
            self.current_cash -= event.commission
        
    def update_orders(self, event):
        
        if event.type != 'SIGNAL':
            return
                
        to_buy = 0
        curr_price = self.bars.current(event.symbol, 'adj_close').item()
        curr_quantity = self.current_holdings[event.symbol]['Quantity']
        
        if event.amount_type == 'SHARES':
            if event.target == False:
                to_buy = event.amount
            elif event.target == True:
                to_buy = event.amount - curr_quantity
                
        elif event.amount_type == 'VALUE':
            if event.target == False:
                to_buy = event.amount / curr_price
            elif event.target == True:
                curr_val = curr_price * curr_quantity
                to_buy = (event.amount - curr_val) / curr_price
                
        elif event.amount_type == 'PERCENTAGE':
            total_value = self.calculate_total_value()
            if event.target == False:
                to_buy = (total_value * event.amount) / curr_price
            elif event.target == True:
                curr_percent = (curr_price * curr_quantity) / total_value
                to_buy = ( total_value * (event.amount - curr_percent) ) / curr_price
                
        else:
            print('Error: invalid amount_type specified, should be SHARES, VALUE, or PERCENTAGE')
            return
        
        if math.isnan(to_buy):
            to_buy = 0
        to_buy = (int)(to_buy)
        
        direction = 'LONG'
        if to_buy < 0:
            direction = 'SHORT'
            
        market_order = OrderEvent(event.symbol, event.order_type, direction, to_buy)
        self.events.put(market_order)

    def calculate_total_value(self):
        return self.calculate_portfolio_value() + self.current_cash
        
    def calculate_portfolio_value(self):
        """
        calculates portfolio value(all open positions) at particular time
        """
        
        value = 0
        for symbol,cost in self.current_holdings.items():
            if not math.isnan(self.current_holdings[symbol]['Price']):
                value += (self.current_holdings[symbol]['Price']*self.current_holdings[symbol]['Quantity'])
                
        return value
                
                
                
                
                
                
                
                
                
                
                
                
            