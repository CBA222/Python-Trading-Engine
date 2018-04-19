# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 01:16:54 2018

@author: blins
"""
import datetime as dt, time
import os, os.path
import pandas as pd
import xarray as xr

from abc import ABCMeta, abstractmethod

from event import MarketEvent

class DataFeed(object):
    """
    Abstract class for DataFeed
    
    latest_bars: gets latest bars of a symbol
    
    update: updates by one time interval all the symbols
    """
    
    @abstractmethod
    def latest_bars(self, symbol, N = 1):
        raise NotImplementedError("Should implement get_latest_bars()")
        
    @abstractmethod    
    def history(self, assets, fields, bar_count, interval, convert_to_pandas):
        raise NotImplementedError("Should implement history()")
        
    @abstractmethod
    def current(self, assets, fields, inteval, convert_to_pandas):
        raise NotImplementedError("Should implement current()")
        
    def update(self):
        raise NotImplementedError("Should implement update_bars()")
        
    # converts dataarray with 2 dimensions to dataframe TWO dimensions only
        
class CSVDataFeed(DataFeed):
    
    def __init__(self, path, events, symbols, time = 0, open = 1, high = 2, low = 3, close = 4, volume = 5):
        self.path = path
        self.events = events
        self.symbols = symbols

        self.keep_iterating = True
        self.data_length = 0

        self.read_from_csv()
        
    def read_from_csv(self):
        not_found = []
        data_list = []
        data_names = []
                
        for s in self.symbols:
            try:
                temp_data = pd.read_csv(os.path.join(self.path, '%s.csv' % s),
                    header=None,
                    names = ['open','high','low','close','adj_close','volume','c7','c8'],
                    index_col=0,
                    parse_dates=True,
                    infer_datetime_format=True)
                temp_data = temp_data.reindex(pd.bdate_range('2018-03-01','2018-03-10'),fill_value=None)      
                temp_data = xr.DataArray(temp_data, dims = ['datetime', 'fields'])
                data_list.append(temp_data)
                data_names.append(s)            
            except IOError:
                not_found.append(s)
                        
        for s in not_found:
            self.symbols.remove(s)
            
        self.data = xr.concat(data_list, dim = pd.Index(data_names).set_names('assets'))
        self.total_length = self.data.sizes['datetime']
        
    def history(self, assets, fields, bar_count, interval = '1d', convert_to_pandas = False):
        start = self.data_length - bar_count
        end = self.data_length
        if convert_to_pandas is False:
            return self.data.isel(datetime=slice(start, end)).sel(fields=fields).sel(assets=assets)
        else:
            return self.data.isel(datetime=slice(start, end)).sel(fields=fields).sel(assets=assets).to_pandas()
    
    def current(self, assets, fields, inteval = '1d', convert_to_pandas = False):
        if convert_to_pandas is False:
            return self.data.isel(datetime=self.data_length).sel(fields=fields).sel(assets=assets)
        else:
            return self.data.isel(datetime=self.data_length).sel(fields=fields).sel(assets=assets).to_pandas()
    
    def update(self):
        if self.data_length >= self.total_length - 1:
            self.keep_iterating = False
        else:
            self.data_length += 1
            self.events.put(MarketEvent())
            
        

    