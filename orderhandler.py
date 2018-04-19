# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 23:19:22 2018

@author: blins
"""

import datetime
#import Queue

from queue import *

from abc import ABCMeta, abstractmethod

from event import FillEvent, OrderEvent
from commission import IBCommission

import math

class OrderHandler(object):
    
    @abstractmethod
    def execute_order(self, event):
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
    
    def execute_order(self, event):
        if event.type == 'ORDER':
            #fill_order = FillEvent(0,event.symbol,'NYSE',1,event.direction,value,self.commission)
            #self.events.put(fill_order)
            pass
            
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
                    fill_order = FillEvent(0,
                                           order.symbol,
                                           self.exchange,
                                           order.quantity,
                                           order.direction,
                                           value,
                                           self.commission.get_commission(order.quantity, price))
                    self.events.put(fill_order)
                    print(order.symbol,order.quantity,order.direction, value)
                
                
                
                
                
                
                
                
            
            