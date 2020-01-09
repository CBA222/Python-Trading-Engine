# Solitude: A Trading Engine in Python

Solitude is a stock trading engine written in Python.

Solitude allows you to perform backtests with historical stock data on custom trading strategies.

## Usage

First, you must implement the Strategy class defined in strategy.py (as a subclass) and put this in a seperate file. Examples can be found in the examples folder. 

### Basic Example
    solitude -st buy_hold.py -sd 01-01-2014 -ed 05-20-2016

This will run a backtest using the strategy defined in buy_hold.py from January 1st, 2014 to May 20th, 2016.

### Additional Options

The choice of starting cash and what commission to use during the backtest are also customizable using the -ch and -cm flags respectively. 

For example:

    solitude -st strategy.py -sd 01-01-2014 -ed 05-20-2016 -cm IB -ch 500



