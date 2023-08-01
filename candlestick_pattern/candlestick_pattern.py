import pandas as pd
import talib
import yfinance
from candle_rankings import candle_rankings
from candle_names import candle_names
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import matplotlib
from itertools import compress
matplotlib.use('TkAgg')
plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)

def data(stocksymbols,start):
    ticker = yfinance.Ticker(stocksymbols)
    end = date.today()
    df = ticker.history(interval="1d",start=start,end=end)
    df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df.index = pd.to_datetime(df.index, errors='coerce')
    df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
    return df



def recognize_candlestick(stocksymbols,start):
    """
    Recognizes candlestick patterns and appends 2 additional columns to df;
    1st - Best Performance candlestick pattern matched by www.thepatternsite.com
    2nd - # of matched patterns
    """
    df = data(stocksymbols,start)
    # extract OHLC
    op = df['Open'].astype(float)
    hi = df['High'].astype(float)
    lo = df['Low'].astype(float)
    cl = df['Close'].astype(float)
    # create columns for each pattern
    candle_names = talib.get_function_groups()['Pattern Recognition']
    for candle in candle_names:
        df[candle] = getattr(talib, candle)(op, hi, lo, cl)

    candle_names = talib.get_function_groups()['Pattern Recognition']
    # patterns not found in the patternsite.com
    exclude_items = ('CDLCOUNTERATTACK',
                     'CDLLONGLINE',
                     'CDLSHORTLINE',
                     'CDLSTALLEDPATTERN',
                     'CDLKICKINGBYLENGTH')
    candle_names = [candle for candle in candle_names if candle not in exclude_items]
    # create columns for each candle
    for candle in candle_names:
        # below is same as;
        # df["CDL3LINESTRIKE"] = talib.CDL3LINESTRIKE(op, hi, lo, cl)
        df[candle] = getattr(talib, candle)(op, hi, lo, cl)
    df['candlestick_pattern'] = np.nan
    df['candlestick_match_count'] = np.nan
    for index, row in df.iterrows():

        # no pattern found
        if len(row[candle_names]) - sum(row[candle_names] == 0) == 0:
            df.loc[index,'candlestick_pattern'] = "NO_PATTERN"
            df.loc[index, 'candlestick_match_count'] = 0
        # single pattern found
        elif len(row[candle_names]) - sum(row[candle_names] == 0) == 1:
            # bull pattern 100 or 200
            if any(row[candle_names].values > 0):
                pattern = list(compress(row[candle_names].keys(), row[candle_names].values != 0))[0] + '_Bull'
                df.loc[index, 'candlestick_pattern'] = pattern
                df.loc[index, 'candlestick_match_count'] = 1
            # bear pattern -100 or -200
            else:
                pattern = list(compress(row[candle_names].keys(), row[candle_names].values != 0))[0] + '_Bear'
                df.loc[index, 'candlestick_pattern'] = pattern
                df.loc[index, 'candlestick_match_count'] = 1
        # multiple patterns matched -- select best performance
        else:
            # filter out pattern names from bool list of values
            patterns = list(compress(row[candle_names].keys(), row[candle_names].values != 0))
            container = []
            for pattern in patterns:
                if row[pattern] > 0:
                    container.append(pattern + '_Bull')
                else:
                    container.append(pattern + '_Bear')
            rank_list = [candle_rankings[p] for p in container]
            if len(rank_list) == len(container):
                rank_index_best = rank_list.index(min(rank_list))
                df.loc[index, 'candlestick_pattern'] = container[rank_index_best]
                df.loc[index, 'candlestick_match_count'] = len(container)
    # clean up candle columns
    cols_to_drop = candle_names + list(exclude_items)
    df.drop(cols_to_drop, axis = 1, inplace = True)
    return df
if __name__ == '__main__':
    a = recognize_candlestick('ITC.NS', '2020-01-01')
    print(a['candlestick_pattern'].tail(30))