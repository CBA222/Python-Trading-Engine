# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 15:55:50 2018

@author: blins
"""

import pandas as pd        

    
class Pipeline(object):
    
    def __init__(self, name):
        self.factors = {}
        self.name = name
        self.asset_list = []
        self.screen = None
        
    def set_screen(self, screen):
        self.screen = screen.loc[screen == True].index
        
    def add_factor(self, col_name, factor):
        self.factors[col_name] = factor
        
    def setup(self):
        
        if self.screen is None:
            self.screen = pd.Index(self.asset_list)
            
        self.table = pd.DataFrame(index = self.screen, columns = list( self.factors.keys() ) )
    
    def calculate_list(self, input_feeds):
        
        for col_name in self.factors:
            f = self.factors[col_name]
            datafeed = input_feeds[f.input]
            data = datafeed.history(self.asset_list, f.window_length)
            self.table[col_name] = f.calculate(data)
        
        self.table = self.table.reindex(self.screen)
        
    def get_output(self):
        return self.table
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
