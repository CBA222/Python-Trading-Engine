# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 01:02:16 2018

@author: blins
"""

class Event(object):
    pass

class MarketEvent(Event):
    
    def __init__(self):
        self.type = 'MARKET'
        
class SignalEvent(Event):
    
    def __init__(self, symbol, amount, amount_type = 'SHARES', target = False, order_type = 'MARKET'):
        self.type = 'SIGNAL'
        self.symbol = symbol
        self.amount = amount
        self.amount_type = amount_type
        self.target = target
        self.order_type = order_type
        
class OrderEvent(Event):
    
    def __init__(self, symbol, order_type, direction, quantity, price = None):
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.direction = direction
        self.quantity = quantity
        self.price = price
        
    def print_order(self):
        print("Ticker:%s, Type:%s, Quantity:%s, Direction:%s" % \
              (self.symbol,self.order_type,self.quantity,self.direction))
        
class FillEvent(Event):
    
    def __init__(self, interval, symbol, exchange, quantity, direction, value, commission):
        self.type = 'FILL'
        self.interval = interval
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.value = value
        self.commission = commission
        
        
        
        
        
        
        
        
        
        
        
        
        