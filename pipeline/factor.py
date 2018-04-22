# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 23:45:54 2018

@author: blins
"""

import pandas as pd
from pipeline.inputs import Input

class Factor(object):
    
    def __init__(self, window_length):
        pass
    
    def calculate(self, *args, **kwargs):
        self.data = pd.Series()
        pass
    
class Returns(Factor):
    
    def __init__(self, window_length = 120, mask = None):
        self.input = Input.price_close
        self.window_length = window_length
        self.mask = mask
        
    def calculate(self, close):
        #self.output = (close.iloc[-1] - close.iloc[0]) / close.iloc[0]
        close = close.T
        return (close.iloc[-1] - close.iloc[0]) / close.iloc[0]
