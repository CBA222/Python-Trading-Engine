# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 01:02:44 2018

@author: blins
"""

class Position(object):
    
    def __init__(self, symbol, shares, price_paid):
        self.symbol = symbol
        self.shares = shares
        self.price_paid = price_paid
        self.price = price_paid
        
    def update(self, new_shares):
        self.shares += new_shares
        