# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 21:53:53 2018

@author: blins
"""

#import Queue

from orderhandler import SimpleOrderHandler
from portfolio import SimplePortfolio
from pipeline.inputs import Input
from pipeline.pipedatafeed import PriceData
from pipeline.pipelineengine import PipelineEngine
import bokeh.plotting
from queue import Queue
import datetime as dt

DEFAULT_CASH = 10000000
DEFAULT_START = dt.date(2003, 1, 1)
DEFAULT_END = dt.date(2018, 1, 1)

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
        
    def set_run_settings(self, cash = DEFAULT_CASH, log_orders = False, start = DEFAULT_START, end = DEFAULT_END):
        self.starting_cash = cash
        self.log_orders = log_orders
        self.start_date = start
        self.end_date = end
        
    def setup_pipeline_data(self, engine):
        base_price_data = self.data.data
        engine.input_datafeeds[Input.price_open] = PriceData(base_price_data.sel(fields='open').to_pandas())
        engine.input_datafeeds[Input.price_high] = PriceData(base_price_data.sel(fields='high').to_pandas())
        engine.input_datafeeds[Input.price_low] = PriceData(base_price_data.sel(fields='low').to_pandas())
        engine.input_datafeeds[Input.price_close] = PriceData(base_price_data.sel(fields='close').to_pandas())
        
    def run(self):
        #setup
        print('Initialized')
        self.data.set_index(self.start_date, self.end_date)
        self.pipeline_engine = PipelineEngine(self.data.symbols)
        self.setup_pipeline_data(self.pipeline_engine)
        
        self.portfolio = SimplePortfolio(self.starting_cash)
        self.portfolio.set_params(self.events,self.data)
        
        self.broker = SimpleOrderHandler(self.events,self.data)
        self.broker.log_orders = self.log_orders
        
        self.strategy.set_params(self.data, self.events, self.portfolio, self.pipeline_engine)
        self.strategy.master_setup()
        self.strategy.setup()        
        
        self.pipeline_engine.setup()
        
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
                    self.pipeline_engine.update(event)
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
                    
                    
                    