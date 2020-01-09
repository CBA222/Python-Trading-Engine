# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 16:00:41 2018

@author: blins
"""

from position import Position

class PositionTracker(object):
    
    def __init__(self):
        self.closed = []
        self.open = {}
        
    def update(self, txn):
        #txn stands for transaction
        if txn.symbol in self.open:
            pos = self.open[txn.symbol]
            if pos.update(txn) == True:
                self.closed.append(pos)
                del self.open[txn.symbol]
        else:
            self.open[txn.symbol] = Position(txn)

    def update_prices(self, bars):
        price_data = bars.current(self.closed, 'adj_close')
        for idx, asset in enumerate(self.open):
            self.open[idx].price = price_data.loc[asset]
            
    
    def calculate_current_value(self, bars):
        total_value = 0
        for asset in self.open:
            total_value += asset.shares * asset.price
        return total_value
        
            
            
                
        