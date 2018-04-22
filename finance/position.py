# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 01:02:44 2018

@author: blins
"""

class Position(object):
        
    def __init__(self, txn):
        self.symbol = txn.symbol
        self.shares = txn.shares
        self.price_paid = txn.value
        self.price = txn.value / txn.shares
        self.start_date = txn.date
        self.closed = False
        
    def update(self, txn):
        self.shares += txn.quantity
        if self.shares == 0:
            self.end_date = txn.date
            self.closed = True
            return True
        else:
            return False
        