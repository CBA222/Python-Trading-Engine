# -*- coding: utf-8 -*-

import abc

class PipelineDatafeed(abc.ABC):
    
    @abc.abstractclassmethod
    def __init__(self, dataset):
        pass
    
    @abc.abstractclassmethod
    def history(self, assets, window_length):
        pass
    

class PriceData(PipelineDatafeed):
    
    def __init__(self, dataset):
        self.dataset = dataset
        
    def history(self, assets, window_length):
        """
        Assume self.dataset is a pandas dataframe
        indexed by asset with dates as columns and containing 
        close price values
        """
        return self.dataset.loc[assets][self.dataset.columns[-window_length:]]
    
        #return self.dataset[self.dataset.columns[assets]].iloc[-window_length:]
    
class FundamentalData(PipelineDatafeed):
    
    def __init__(self, dataset):
        self.dataset = dataset
        
    def history(self, assets, window_length):
        pass
    
    
    
    