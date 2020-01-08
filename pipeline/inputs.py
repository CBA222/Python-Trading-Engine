# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 00:06:54 2018

@author: blins
"""

from enum import Enum

class Input(Enum):
    pass
    
class PriceInput(Input):
    
    price_open = 1
    price_high = 2
    price_low = 3
    price_close = 4

class FundamentalInput(Input):
    
    PE_Ratio = 1
    Revenue = 2

