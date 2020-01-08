import argparse
import datetime as dt
import importlib
import inspect
import os
import pandas as pd
from datafeed import CSVDataFeed

from trader import Trader
from commission import IBCommission
from strategy import Strategy

from example_strategies import Momentum

DEFAULT_CASH = 50000
DEFAULT_COMMISSION = IBCommission()

COMMISSIONS = {
    'IB': IBCommission
}

def check_date(x):
    """
    Checks if the given string x is in a valid date format

    Valid format: MM-DD-YYYY
    """

    if len(x) != 10:
        raise argparse.ArgumentTypeError('Date should be in format MM-DD-YYYY')

    try:
        month = int(x[0:2])
        day = int(x[3:5])
        year = int(x[6:10])
        date = dt.datetime(year, month, day)

    except ValueError:
        raise argparse.ArgumentTypeError('Not a valid date')

    return date
    #return x

def check_strategy(x):
    """
    Checks if the given string is a valid path to python file
    """
    module_name = x.split('.')[0]
    strategy_file = importlib.import_module(module_name)
    strategy = inspect.getmembers(strategy_file)[1][1]
    assert(issubclass(strategy, Strategy))

    return strategy

def check_commission(x):
    """
    Checks if the given string is a valid commission name
    """
    if x not in COMMISSIONS.keys():
        raise argparse.ArgumentTypeError('Not a valid commission name')

    return COMMISSIONS[x]()

def check_cash(x):
    """
    Checks if the given string is in the form of an positive integer
    """

    try:
        cash = int(x)
        if cash <= 0:
            raise argparse.ArgumentTypeError('Argument should be in the form of a positive integer')
    except ValueError:
        raise argparse.ArgumentTypeError('Argument should be in the form of a positive integer')

    return cash


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-st', dest='strategy', type=check_strategy, required=True, help="Python file containing a implementation of the Strategy class")
    parser.add_argument('-sd', dest='start_date', type=check_date, required=True, help="Start date of the backtest")
    parser.add_argument('-ed', dest='end_date', type=check_date, required=True, help="End date of the backtest")
    parser.add_argument('-cm', dest='commission', type=check_commission, default='IB', help="Choice of backtest commission. Valid options: 'IB'")
    parser.add_argument('-ch', dest='cash', type=check_cash, default='50000', help="Backtest starting cash (must be a positive integer)")

    args = parser.parse_args()

    print(args.strategy)


    # Run backtest

    trader = Trader()

    path = os.path.dirname(os.path.realpath(__file__))
    subdirs = next(os.walk(path))[1]

    idx = subdirs.index('data')
    data_path = os.path.join(path, subdirs[idx])

    file = pd.read_csv('tickers.txt', sep=',')
    symbols = set(file['Symbol'].tolist())
    data = CSVDataFeed(data_path, trader.events, symbols)

    trader.add_data(data)
    trader.set_strategy(args.strategy())
    trader.set_run_settings(cash = args.cash,
                            log_orders = False,
                            start = args.start_date,
                            end = args.end_date,
                            commission = args.commission
                            )
    
    trader.run()

    trader.results()