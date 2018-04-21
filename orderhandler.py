# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 23:19:22 2018

@author: blins
"""

from queue import Queue
from event import FillEvent
from commission import IBCommission

import abc
import math

class OrderHandler(object, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def execute_pending(self, event):
        pass
    
    @abc.abstractmethod
    def send_order(self, event):
        pass
    
class SimpleOrderHandler(OrderHandler):
    """
    A simple order handler
    It uses Interactive Brokers commission structure(by default)
    Fills all orders at next closing bar price(currently only supports market orders)
    """
    
    def __init__(self, events, data, commission = IBCommission()):
        self.events = events
        self.commission = commission
        self.pending_orders = Queue()
        self.data = data        
        self.exchange = 'NYSE'
        self.log_orders = False
        self.interval = 0
        
    def activate_logging(self):
        self.log_orders = True
        
    def deactivate_logging(self):
        self.log_orders = False
            
    def send_order(self, event):
        if event.type == 'ORDER':
            self.pending_orders.put(event)
            
    def execute_pending(self, event):
        if event.type != 'MARKET':
            return

        while not self.pending_orders.empty():
            order = self.pending_orders.get()
            if order.order_type is 'MARKET':
                price = self.data.current(order.symbol,fields='adj_close').item()
                if not math.isnan(price):
                    value = price * order.quantity #next/current time closing price
                    fill_order = FillEvent(self.interval,
                                           order.symbol,
                                           self.exchange,
                                           order.quantity,
                                           order.direction,
                                           value,
                                           self.commission.get_commission(order.quantity, price))
                    self.events.put(fill_order)
                    if self.log_orders == True:
                        print(order.symbol,order.quantity,order.direction, value)
                
                
                
                
                
                
                
                
            
            