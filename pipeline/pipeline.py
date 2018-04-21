# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 15:55:50 2018

@author: blins
"""

import pandas as pd

class Factor(object):
    
    def __init__(self, window_length):
        pass
    
    def pass_data(self, inputs):
        pass
    
    def calculate(self, *args, **kwargs):
        
        pass
    
class Returns(Factor):
    
    def __init__(self, window_length = 120):
        self.window_length = window_length
        
    def calculate(self):
        pass
    
class Pipeline(object):
    
    def __init__(self, bars, name):
        self.pipe = pd.DataFrame()
        self.factors = []
        self.bars = bars
        self.name = name
    
    def set_screen(self, screen):
        self.screen = screen.loc[screen == True].index
        
    def add_factor(self, factor):
        self.factors.append(factor)
    
    def calculate_list(self):
        
        self.pipe = pd.DataFrame(index = self.bars.data.index)
        self.pipe = self.pipe.reindex(self.screen)
        
        
        
    def get_output(self):
        return self.pipe
        
    
