# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 16:02:23 2018

@author: blins
"""

class Transaction(object):
    
    def __init__(self, event, date):
        self.symbol = event.symbol
        self.value = event.value
        self.shares = event.quantity
        self.commission = event.commission
        self.date = date
        
    