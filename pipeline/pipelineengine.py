# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 18:43:57 2018

@author: blins
"""

#from pipeline import Pipeline
#from pipedatafeed import PriceData, FundamentalData


class PipelineEngine(object):
    
    def __init__(self, asset_list):
        self.input_datafeeds = dict()
        self.master_list = asset_list
        self.attached = False
        
    def setup(self):
        if self.attached == True:
            self.pipeline.asset_list = self.master_list
            self.pipeline.setup()
    
    def add_pipeline(self, pipeline):
        self.pipeline = pipeline
        self.attached = True
        
    def update(self, event):
        for feed in self.input_datafeeds:
            self.input_datafeeds[feed].update()
        
        if self.attached == True:
            self.pipeline.calculate_list(self.input_datafeeds)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
        
    