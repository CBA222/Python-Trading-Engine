# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 21:45:43 2018

@author: blins
"""

import copy
import pandas_market_calendars as mcal
from event import OrderEvent
import math
import pandas as pd

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
    
class SimplePortfolio(Portfolio):
    
    def __init__(self, starting_capital):
        """
        all_holdings is a list holding nested dictionaries
        Each list element represents one unit of time, inside it is a dictionary
        listing the current holdings of each symbol, as well as the current cash
        
        current_holdings hold the most recent dictionary
        
        """
        
        self.all_holdings = {}
        self.current_cash = 0
        self.starting_capital = starting_capital
        self.default_quantity = 1
        
        self.positions = []
        
    def setup(self):
        #create initial holdings

        date_idx = self.bars.date_idx
        self.symbol_list = self.bars.data.sel(fields='close').to_pandas().index
        
        self.all_holdings['Quantity'] = pd.DataFrame(0, index = date_idx, columns = self.symbol_list)   
        self.all_holdings['Price'] = pd.DataFrame(0, index = date_idx, columns = self.symbol_list) 
        self.all_cash = pd.Series(0, index = date_idx)
        self.curr_pos = 0
        
        self.current_holdings = pd.Series(0, index = self.symbol_list)
        self.current_cash = self.starting_capital
        
        self.returns = pd.Series(0.0, index = date_idx)
        self.history = pd.Series(0.0, index = date_idx)
        
        self.total_returns = pd.Series(0.0, index = date_idx)
        
    def update_holdings(self):
        """
        Updates the prices for the Portfolio's holdings according to current market close
        
        all_holdings contains all previous holdings + current_holdings
        
        This function creates a new current_holding based on current prices and appends it to all_holdings
        """
        
        self.all_holdings['Quantity'].iloc[self.curr_pos] = self.current_holdings
        self.all_holdings['Price'].iloc[self.curr_pos] = self.bars.current(self.symbol_list, 'adj_close')
        self.all_cash[self.curr_pos] = self.current_cash
        
        self.total_returns[self.curr_pos] = (100 * (self.calculate_total_value() / self.starting_capital)) - 100
        
        self.history[self.curr_pos] = self.calculate_total_value()
        if self.curr_pos > 0:
            prev = self.history[self.curr_pos - 1]
            self.returns[self.curr_pos] = self.history[self.curr_pos] / prev
            
        self.curr_pos += 1
        
        
    def update_fill(self, event):
        
        if event.type != 'FILL':
            return
        
        direction = 0
        if event.quantity >= 0:
            direction = 1
        elif event.quantity < 0:
            direction = -1
        
        self.current_holdings.loc[event.symbol] += (event.quantity)
        self.current_cash -= event.value * direction
        self.current_cash -= event.commission
        
        
    def update_orders(self, event):
        
        if event.type != 'SIGNAL':
            return
                
        to_buy = 0
        curr_price = self.bars.current(event.symbol, 'adj_close').item()
        curr_quantity = self.current_holdings.loc[event.symbol]
        
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
        value = (self.current_holdings * self.bars.current(self.symbol_list, 'adj_close')).sum()
        return value
    
    def open_positions(self):
        return pd.concat([self.current_holdings.loc[self.current_holdings > 0],
                         self.current_holdings.loc[self.current_holdings < 0]])
                
                
                
                
                
                
                
                
                
                
                
            
