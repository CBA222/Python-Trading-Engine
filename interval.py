# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 23:27:43 2018

@author: blins
"""

from datetime import timedelta

#Representation in number of seconds
INTERVAL_TYPES = {
        'D': 86400,
        'd': 86400,
        'H': 3600,
        'h': 3600,
        'M': 60,
        'm': 60,
        'S': 1,
        's': 1
        }

def get_time_delta(input_str):
    
    interval_unit = input_str[-1]
        
    if interval_unit in INTERVAL_TYPES:
        num_units = (int)(input_str[0:-1])
        return timedelta(seconds = INTERVAL_TYPES[interval_unit] * num_units)
        
    else:
        print('Error: interval unit not valid, should be D, H, M, or S')

class Interval(object):
    
    def __init__(self, input_str):
        
        interval_unit = input_str[-1]
        
        if interval_unit in INTERVAL_TYPES:
            num_units = (int)(input_str[0:-1])
            self.time_delta = timedelta(seconds = INTERVAL_TYPES[interval_unit] * num_units)
            
        else:
            print('Error: interval unit not valid, should be D, H, M, or S')
        
    