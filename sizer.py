# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 13:23:26 2018

@author: blins
"""
import math

class Sizer(object):
    """
    Used by the portfolio object to determine number of shares to buy
    Usually defined within strategy class
    """
    def return_size(self):
        pass

class EqualPercentageSizer(Sizer):
    """
    """
    def __init__(self,portfolio,strategy,bars,percentage):
        self.portfolio = portfolio
        self.strategy = strategy
        self.bars = bars
        self.percentage = percentage
        
    def return_size(self,symbol):
        share_price = self.bars.bar_back(symbol,0)[5]
        if math.isnan(share_price):
            return 0
        portfolio_total_value = self.portfolio.calculate_portfolio_value() + self.portfolio.current_cash
        target_value = portfolio_total_value*self.percentage
        target_quantity = target_value/share_price
        return int(round(target_quantity))
            