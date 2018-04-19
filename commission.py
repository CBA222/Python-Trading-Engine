# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 23:15:20 2018

@author: blins
"""

class Commission(object):
    
    def get_commission(self, shares, share_price):
        pass

class IBCommission(Commission):
    
    def __init__(self):
        self.min = 1.00
        self.fixed = 0.005
        self.max_share = 0.01
    
    def get_commission(self, shares, share_price):
        max_comm = ( shares * share_price ) * self.max_share
        base_value = shares * self.fixed
        if base_value < self.min:
            return self.min
        elif base_value > max_comm:
            return max_comm
        else:
            return base_value
        
class FixedCommission(Commission):
    
    def __init__(self, fixed):
        self.fixed = fixed
        
    def get_commission(self, shares, share_price):
        return self.fixed
        
class FixedPercentageCommission(Commission):
    
    def __init__(self, percent):
        self.percent = percent
        
    def get_commission(self, shares, share_price):
        return (shares * share_price) * self.percent
        
        
        
        
        
        
        
        
        
    