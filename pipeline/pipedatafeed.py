# -*- coding: utf-8 -*-

import abc

class PipelineDatafeed(abc.ABC):
    """
    A PipelineDatafeed object is responsible for holding the raw data
    used underlying a certain pipeline factor
    
    Each PipelineDatafeed corresponds to a pipeline factor
    """
    
    @abc.abstractclassmethod
    def __init__(self, dataset):
        pass
    
    @abc.abstractclassmethod
    def history(self, assets, window_length):
        pass
    
    @abc.abstractclassmethod
    def update(self):
        pass

class PriceData(PipelineDatafeed):
    
    def __init__(self, dataset):
        self.dataset = dataset
        self.data_length = 0
        self.interval = '1d'
        
    def history(self, assets, window_length):
        """
        Assume self.dataset is a pandas dataframe
        indexed by asset with dates as columns and containing 
        close price values
        """
        return self.dataset.loc[assets][self.dataset.columns[(self.data_length - window_length):self.data_length]]
        #return self.dataset.loc[assets][self.dataset.columns[-window_length:]]
    
        #return self.dataset[self.dataset.columns[assets]].iloc[-window_length:]
        
    def update(self):
        self.data_length += 1
    
class FundamentalData(PipelineDatafeed):
    
    def __init__(self, dataset):
        self.dataset = dataset
        
    def history(self, assets, window_length):
        pass
    
    
    
    