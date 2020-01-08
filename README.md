# Python-Trading-Engine
A trading engine in Python.

This program allows you to perform backtests on custom trading strategies built in python. 

## Usage

### Basic Example
    solitude -i strategy.py -sd 01-01-2014 -ed 05-20-2016

This will run a backtest using the strategy defined in strategy.py from January 1st, 2014 to May 20th, 2016.

### Additional Options

The choice of starting cash and what commission to use during the backtest are also customizable using the -ch and -cm flags respectively. 

For example:

    solitude -i strategy.py -sd 01-01-2014 -ed 05-20-2016 -cm IB -ch 500



