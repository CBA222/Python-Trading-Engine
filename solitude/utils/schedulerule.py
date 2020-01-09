# -*- coding: utf-8 -*-

"""
schedule_rule.py
"""

import abc

class ScheduleRule(object, metaclass = abc.ABCMeta):
    
    """
    Return whether or not to execute function on date provided
    """
    
    @abc.abstractclassmethod
    def on_date(self, date, index, starts):
        pass
    
class n_days(ScheduleRule):
    
    def __init__(self, N = 1):
        self.N = N
        self.time_since_last = 0
        
    def on_date(self, date, index, starts):
        if self.time_since_last >= self.N - 1:
            self.time_since_last = 0
            return True
        else:
            self.time_since_last += 1
            return False     
    
class every_month(ScheduleRule):
    
    def __init__(self, offset = 0):
        self.offset = offset
        
    def on_date(self, date, index, starts):
        return index[index.get_loc(date) - self.offset] in starts['month']
    
class every_week(ScheduleRule):
    
    def __init__(self, offset = 0):
        self.offset = offset
        
    def on_date(self, date, index, starts):
        return index[index.get_loc(date) - self.offset] in starts['week']

class n_months(ScheduleRule):
    
    def __init__(self, offset = 0, N = 1):
        self.offset = offset
        self.time_since_last = 0
        self.N = N
        
    def on_date(self, date, index, starts):
        if index[index.get_loc(date) - self.offset] in starts['month']:
            if self.time_since_last >= self.N - 1:
                self.time_since_last = 0
                return True
            else:
                self.time_since_last += 1
                return False
            
class n_weeks(ScheduleRule):
    
    def __init__(self, offset = 0, N = 1):
        self.offset = offset
        self.time_since_last = 0
        self.N = N
        
    def on_date(self, date, index, starts):
        if index[index.get_loc(date) - self.offset] in starts['week']:
            if self.time_since_last >= self.N - 1:
                self.time_since_last = 0
                return True
            else:
                self.time_since_last += 1
                return False        
        
        
        
        
        