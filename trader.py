# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 21:53:53 2018

@author: blins
"""

#import Queue

from orderhandler import SimpleOrderHandler
from portfolio import SimplePortfolio
import bokeh.plotting
from queue import Queue

DEFAULT_CASH = 10000000

class Trader(object):
    """
    class managing event driven loop
    """   
    
    def __init__(self):
        self.events = Queue()
        self.starting_cash = DEFAULT_CASH
        self.log_orders = False
    
    def add_data(self, data):
        self.data = data
        
    def add_strategy(self, strat):
        self.strategy = strat
        
    def set_commission(self, commission):
        self.commission = commission
        
    def set_portfolio(self, portfolio):
        self.portfolio = portfolio
        
    def set_starting_cash(self, cash):
        self.starting_cash = cash
        
    def set_run_settings(self, log_orders = False):
        self.log_orders = log_orders
        
    def run(self):
        #setup
        print('Initialized')
        self.portfolio = SimplePortfolio(self.starting_cash)
        self.portfolio.set_params(self.events,self.data)
        self.broker = SimpleOrderHandler(self.events,self.data)
        self.broker.log_orders = self.log_orders
        
        self.strategy.set_params(self.data, self.events, self.portfolio)
        self.strategy.master_setup()
        self.strategy.setup()        
        self.data.set_index(self.strategy.start_date, self.strategy.end_date)

        self.portfolio.setup()
        
        while True:
            if self.data.keep_iterating == True:
                self.data.update()
            else:
                break
            
            while True:
                if self.events.empty():
                    break
                else:
                    event = self.events.get()
                    
                if event.type == 'MARKET':
                    self.strategy.get_signals(event)
                    self.strategy.execute_scheduled_functions(event)
                    self.broker.execute_pending(event)
                    
                if event.type == 'SIGNAL':
                    self.portfolio.update_orders(event)
                    
                if event.type == 'ORDER':
                    self.broker.send_order(event)
                    
                if event.type == 'FILL':
                    self.portfolio.update_fill(event)
                
            self.portfolio.update_holdings()
            self.strategy.log_vars()
                
                    
    def results(self):
        print('Final Portfolio Value: %.2f' % self.portfolio.calculate_portfolio_value())
        print('Final Cash Value: %.2f' % self.portfolio.current_cash)
        total = self.portfolio.calculate_portfolio_value() + self.portfolio.current_cash
        print("Total Value: %.2f" % total)
        print("Absolute Return: %.2f %%" % self.portfolio.total_returns[-1])
                    
    def plot(self):
        bokeh.plotting.output_file("chart.html", title="Equity Curve")
        p = bokeh.plotting.figure(x_axis_type="datetime", plot_width=1000, plot_height=400, title="Equity Curve")
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Percentage Return'
        p.line(self.portfolio.total_returns.index, self.portfolio.total_returns)
        bokeh.plotting.show(p)
                    
                    
                    