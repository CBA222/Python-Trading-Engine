# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 16:46:07 2018

@author: blins
"""

import pandas as pd

class Benchmark(object):
    
    def __init__(self, symbol, date_idx):
        self.symbol = symbol
        self.total_returns = pd.Series(0.0, index = date_idx)
        self.curr_pos = 0
        
    def set_params(self, bars):
        self.bars = bars
        
    def setup(self):
        self.starting_price = self.bars.current(self.symbol, 'adj_close')
        
    def update(self):
        self.total_returns[self.curr_pos] = self.bars.current(self.symbol, 'adj_close').item() / self.starting_price