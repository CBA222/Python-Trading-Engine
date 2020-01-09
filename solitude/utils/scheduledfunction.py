# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 02:42:36 2018

@author: blins
"""

class ScheduledFunction(object):
    
    def __init__(self, function, sch_rule):
        self.function = function
        self.sch_rule = sch_rule #schedule rule
        
    def on_date(self, date, index, starts):
        return self.sch_rule.on_date(date, index, starts)