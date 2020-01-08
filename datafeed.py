# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 01:16:54 2018

@author: blins
"""
import datetime as dt, time
import pandas_market_calendars as mcal
import os, os.path
import pandas as pd
import xarray as xr

#from abc import ABCMeta, abstractmethod
import abc

from event import MarketEvent
from interval import Interval
from utils.timestarts import get_month_starts, get_week_starts

INTERVALS = {
        '1_DAY': Interval('1d'),
        '1_HOUR': Interval('1h'),
        '1_MIN': Interval('1m'),
        '1_SEC': Interval('1s')
        }

class DataFeed(object, metaclass=abc.ABCMeta):
    """
    A class that represents a datafeed of chronological price data.

    A datafeed should keep track of the current chronological time, as well as 
    store the price history of all the time up to the current time.

    ...

    Methods
    -------
    history()
        Return price history for the given assets, fields, and time period
    current()
        Return the current price for the given assets and fields.
    update()
        Advance the current chronological time by one unit (e.g. 1 day)
    current_date()
        Return the current time of the datafeed
    """
        
    @abc.abstractmethod    
    def history(self, assets, fields, bar_count, interval, convert_to_pandas):
        raise NotImplementedError("Should implement history()")
        
    @abc.abstractmethod
    def current(self, assets, fields, inteval, convert_to_pandas):
        raise NotImplementedError("Should implement current()")
        
    @abc.abstractmethod    
    def update(self):
        raise NotImplementedError("Should implement update_bars()")
        
    @abc.abstractclassmethod
    def current_date(self):
        raise NotImplementedError("Should implement current_date(()")

        
class CSVDataFeed(DataFeed):
    """
    CSVDataFeed implements the Datafeed class. 
    """
    
    def __init__(self, path, events, symbols, interval = INTERVALS['1_DAY'], 
                 open = 1, high = 2, low = 3, close = 4, volume = 5):
        self.path = path
        self.events = events
        self.symbols = symbols
        self.fields = ['open','high','low','close','adj_close','volume']
        self.interval = interval

        self.keep_iterating = True
        self.data_length = 0
        self.default_start_date = dt.date(2018, 1, 1)
        self.default_end_date = dt.date(2018, 3, 1)
        
        self.hard_start = dt.date(1995, 1, 1)
        self.hard_stop = dt.date(2020, 1, 1)
        self.read_from_csv()
        
        
    def set_start_date(self, date):
        self.start_date = date
    
    def set_end_date(self, date):
        self.end_date = date
        
    def set_index(self, start, end):
        schedule = mcal.get_calendar('NYSE').schedule(start_date=start, end_date=end)
        idx = mcal.date_range(schedule, frequency='1d').to_period('1d').to_timestamp()
        self.data = self.data.reindex(datetime = idx)
        self.date_idx = idx
        self.total_length = self.data.sizes['datetime']
        
        self.starts = dict()
        self.starts['month'] = get_month_starts(self.date_idx)
        self.starts['week'] = get_week_starts(self.date_idx)
        
    def read_from_csv(self):
        not_found = []
        data_list = []
        data_names = []
        
        schedule = mcal.get_calendar('NYSE').schedule(start_date=self.hard_start, end_date=self.hard_stop)
        date_idx = mcal.date_range(schedule, frequency='1d').to_period('1d').to_timestamp()
        
        for s in self.symbols:
            try:
                temp_data = pd.read_csv(os.path.join(self.path, '%s.csv' % s),
                    header = None,
                    names = ['open','high','low','close','adj_close','volume','c7','c8'],
                    index_col = 0,
                    parse_dates = True,
                    infer_datetime_format = True)
                #temp_data = temp_data.reindex(pd.bdate_range(self.start_date,self.end_date),fill_value=None)
                temp_data = temp_data.reindex(date_idx, fill_value=None)
                temp_data = xr.DataArray(temp_data, dims = ['datetime', 'fields'])
                data_list.append(temp_data)
                data_names.append(s)            
            except IOError:
                not_found.append(s)
                        
        for s in not_found:
            self.symbols.remove(s)
            
        self.data = xr.concat(data_list, dim = pd.Index(data_names).set_names('assets'))
        
    def history(self, assets, fields, bar_count, interval = '1d', convert_to_pandas = True):
        
        #assets = [a for a in assets if a in set(self.symbols)]
        #fields = [f for f in fields if f in set(self.fields)]
        
        start = self.data_length - bar_count
        end = self.data_length
        
        hist_data = self.data.isel(datetime=slice(start, end)).sel(fields=fields).sel(assets=assets)
        
        if convert_to_pandas is False:
            return hist_data
        else:
            return hist_data.to_pandas()
    
    def current(self, assets, fields, inteval = '1d', convert_to_pandas = True):
        
        #assets = [a for a in assets if a in set(self.symbols)]
        #fields = [f for f in fields if f in set(self.fields)]
        
        curr_data = self.data.isel(datetime=self.data_length).sel(fields=fields).sel(assets=assets)
        
        if convert_to_pandas is False:
            return curr_data
        else:
            return curr_data.to_pandas()
        
    def current_date(self):
        return self.date_idx[self.data_length]
    
    def update(self):
        
        if self.data_length >= self.total_length - 1:
            self.keep_iterating = False
        else:
            self.data_length += 1
            self.events.put(MarketEvent())
            
        

    