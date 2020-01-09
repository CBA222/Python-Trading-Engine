# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 02:13:02 2018

@author: blins
"""

from .progressbar import update_progress
import time



class Foo(object):
    
    def run(self):
        i = 0
        while(True):
            time.sleep(0.1)
            i += 1
            if i >= 100:
                break
            update_progress(i/100.0)