import pandas as pd
import yfinance
import plotly.graph_objects as go
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from datetime import date
import matplotlib
matplotlib.use('TkAgg')
plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)


def data(stocksymbols):
    ticker = yfinance.Ticker(stocksymbols)
    end = date.today()
    df = ticker.history('max')

    df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df.index = pd.to_datetime(df.index, errors='coerce')
    df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

    return df


def plot_candlestick(stocksymbols):
    df = data(stocksymbols)
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

    fig.show()



if __name__ == '__main__':

    stocksymbols = 'LT.NS'
    plot_candlestick(stocksymbols)
