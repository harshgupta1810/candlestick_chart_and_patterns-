import pandas as pd
import yfinance
import numpy as np
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from datetime import date
import matplotlib
from scipy.signal import argrelextrema
from statsmodels.nonparametric.kernel_regression import KernelReg
matplotlib.use('TkAgg')
plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)


def get_data(ticker,start_date):
    ticker = yfinance.Ticker(ticker)
    end = date.today()
    df = ticker.history(interval="1d", start=start_date, end=end)
    df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df.index = pd.to_datetime(df.index, errors='coerce')
    df.index = df.index.strftime('%d-%m-%y')
    df.drop(columns=['Date'])
    df = df.loc[:, ['Close']]


    return df


def find_extrema(ticker,start_date, bw='cv_ls'):
    """
    Input:
        s: prices as pd.series
        bw: bandwith as str or array like
    Returns:
        prices: with 0-based index as pd.series
        extrema: extrema of prices as pd.series
        smoothed_prices: smoothed prices using kernel regression as pd.series
        smoothed_extrema: extrema of smoothed_prices as pd.series
    """
    # Copy series so we can replace index and perform non-parametric
    # kernel regression.
    s = get_data(ticker,start_date)
    prices = s.copy()
    prices = prices.reset_index()
    prices.columns = ['date', 'price']
    prices = prices['price']

    kr = KernelReg([prices.values], [prices.index.to_numpy()], var_type='c', bw=bw)
    f = kr.fit([prices.index])

    # Use smoothed prices to determine local minima and maxima
    smooth_prices = pd.Series(data=f[0], index=prices.index)
    smooth_local_max = argrelextrema(smooth_prices.values, np.greater)[0]
    smooth_local_min = argrelextrema(smooth_prices.values, np.less)[0]
    local_max_min = np.sort(np.concatenate([smooth_local_max, smooth_local_min]))
    smooth_extrema = smooth_prices.loc[local_max_min]

    # Iterate over extrema arrays returning datetime of passed
    # prices array. Uses idxmax and idxmin to window for local extrema.
    price_local_max_dt = []
    for i in smooth_local_max:
        if (i>1) and (i<len(prices)-1):
            price_local_max_dt.append(prices.iloc[i-2:i+2].idxmax())

    price_local_min_dt = []
    for i in smooth_local_min:
        if (i>1) and (i<len(prices)-1):
            price_local_min_dt.append(prices.iloc[i-2:i+2].idxmin())

    maxima = pd.Series(prices.loc[price_local_max_dt])
    minima = pd.Series(prices.loc[price_local_min_dt])
    extrema = pd.concat([maxima, minima]).sort_index()

    # Return series for each with bar as index
    return extrema, prices, smooth_extrema, smooth_prices



def plot_extrema(ticker,start_date, ax=None):
    extrema, prices, smooth_extrema, smooth_prices = find_extrema(ticker,start_date)
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    prices.plot(ax=ax, color='dodgerblue')
    ax.scatter(extrema.index, extrema.values, color='red')
    smooth_prices.plot(ax=ax, color='lightgrey')
    ax.scatter(smooth_extrema.index, smooth_extrema.values, color='lightgrey')
    plt.show()


if __name__ == '__main__':
    extrema, prices, smooth_extrema, smooth_prices = find_extrema('LT.NS','2023-01-01')
    print(f'prices: {len(prices)}')
    print(f'extrema: {len(extrema)}')
    print(f'smooth_prices: {len(smooth_prices)}')
    print(f'smooth_extrema: {len(smooth_extrema)}')
    plot_extrema('LT.NS', '2020-01-01')
