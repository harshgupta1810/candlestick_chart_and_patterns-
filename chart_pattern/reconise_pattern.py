from collections import defaultdict
import matplotlib.dates as mpl_dates
import pandas as pd
from datetime import date
import numpy as np
import yfinance as yf
from find_extrema import find_extrema


def get_data(ticker,start_date):
    ticker = yf.Ticker(ticker)
    end = date.today()
    df = ticker.history(interval="1d", start=start_date, end=end)
    df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df.index = pd.to_datetime(df.index, errors='coerce')
    df.index = df.index.strftime('%d-%m-%y')
    df = df.loc[:, ['Close']]
    return df

def find_patterns(ticker,start_date, max_bars=35):
    """
    Input:
        s: extrema as pd.series with bar number as index
        max_bars: max bars for pattern to play out
    Returns:
        patterns: patterns as a defaultdict list of tuples
        containing the start and end bar of the pattern
    """
    extrema, prices, smooth_extrema, smooth_prices =  find_extrema(ticker,start_date)
    patterns = defaultdict(list)

    # Need to start at five extrema for pattern generation
    for i in range(7, len(smooth_extrema)):
        window = smooth_extrema.iloc[i - 7:i]

        # A pattern must play out within max_bars (default 35)
        if (window.index[-1] - window.index[0]) > max_bars:
            continue

        # Using the notation from the paper to avoid mistakes
        e1 = window.iloc[0]
        e2 = window.iloc[1]
        e3 = window.iloc[2]
        e4 = window.iloc[3]
        e5 = window.iloc[4]
        e6 = window.iloc[5]
        e7 = window.iloc[6]
        pattern_found = False  # set to True when a pattern is found
        # Head and Shoulders
        if (e2 > e1) and (e2 > e3) and \
                (e4 < e1) and (e4 < e5) and \
                (e6 < e3) and (e6 < e5) and \
                (e2 - min(e1, e3) >= 0.03 * np.mean([e1, e3])) and \
                (max(e4, e6) - e5 <= 0.05 * np.mean([e4, e6])):
            patterns['Head_and_Shoulders'].append((window.index[0], window.index[-1]))
        # Inverse Head and Shoulders
        if (e2 < e1) and (e2 < e3) and \
                (e4 > e1) and (e4 > e5) and \
                (e6 > e3) and (e6 > e5) and \
                (max(e1, e3) - e2 >= 0.03 * np.mean([e1, e3])) and \
                (e5 - min(e4, e6) <= 0.05 * np.mean([e4, e6])):
            patterns['Inverse_Head_and_Shoulders'].append((window.index[0], window.index[-1]))

        # Bullish_Flag
        if (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (e1 < e3) and (e2 < e3) and (e4 < e3) and (e5 < e3):
            patterns['Bullish_Flag'].append((window.index[0], window.index[-1]))

        # Bearish_Flag
        if (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (e1 > e3) and (e2 > e3) and (e4 > e3) and (e5 > e3):
            patterns['Bearish_Flag'].append((window.index[0], window.index[-1]))

        # Bullish_Pennant
        if (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (e1 < e2) and (e5 < e4) and (e2 < e3) and (e4 < e3):
            patterns['Bullish_Pennant'].append((window.index[0], window.index[-1]))

        # Bearish_Pennant
        if (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (e1 > e2) and (e5 > e4) and (e2 > e3) and (e4 > e3):
            patterns['Bearish_Pennant'].append((window.index[0], window.index[-1]))

        # Ascending_Triangle
        if (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (e1 < e3) and (e2 > e4) and (e5 < e3) and \
                (abs(e2 - e3) <= 0.03 * np.mean([e2, e3])) and \
                (abs(e4 - e3) <= 0.03 * np.mean([e3, e4])):
            patterns['Ascending_Triangle'].append((window.index[0], window.index[-1]))

        # Descending_Triangle
        if (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (e1 > e3) and (e2 < e4) and (e5 > e3) and \
                (abs(e2 - e3) <= 0.03 * np.mean([e2, e3])) and \
                (abs(e4 - e3) <= 0.03 * np.mean([e3, e4])):
            patterns['Descending_Triangle'].append((window.index[0], window.index[-1]))

        # Bullish_Channel
        if (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (e1 < e3) and (e5 > e3) and \
                (abs(e2 - e3) <= 0.03 * np.mean([e2, e3])) and \
                (abs(e4 - e3) <= 0.03 * np.mean([e3, e4])):
            patterns['Bullish_Channel'].append((window.index[0], window.index[-1]))

        # Bearish_Channel
        if (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (e1 > e3) and (e5 < e3) and \
                (abs(e2 - e3) <= 0.03 * np.mean([e2, e3])) and \
                (abs(e4 - e3) <= 0.03 * np.mean([e3, e4])):
            patterns['Bearish_Channel'].append((window.index[0], window.index[-1]))

        # Horizontal_Channel
        if (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (abs(e1 - e3) <= 0.03 * np.mean([e1, e3, e5])) and \
                (abs(e4 - e5) <= 0.03 * np.mean([e1, e3, e5])):
            patterns['Horizontal_Channel'].append((window.index[0], window.index[-1]))

        # Cup_with_Handle
        if (e1 < e2) and (e3 < e2) and (e4 < e2) and (e5 < e2) and \
                (abs(e1 - e3) <= 0.1 * np.mean([e1, e3, e5])) and \
                (abs(e4 - e2) <= 0.1 * np.mean([e1, e3, e5])) and \
                (abs(e5 - e2) <= 0.1 * np.mean([e1, e3, e5])) and \
                (abs(e1 - e5) <= 0.3 * np.mean([e1, e3, e5])) and \
                (e6 > np.mean([e1, e3, e5])) and (e7 > np.mean([e1, e3, e5])) and \
                (abs(e6 - e7) <= 0.1 * np.mean([e6, e7])):
            patterns['Cup_with_Handle'].append((window.index[0], window.index[-1]))

        # Symmetrical_Triangle
        if (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (abs(e1 - e3) <= 0.03 * np.mean([e1, e3, e5])) and \
                (abs(e4 - e5) <= 0.03 * np.mean([e1, e3, e5])) and \
                ((e2 < e4 and e2 < e1 and e2 < e3 and e4 < e5) or \
                 (e2 > e4 and e2 > e1 and e2 > e3 and e4 > e5)):
            patterns['Symmetrical_Triangle'].append((window.index[0], window.index[-1]))

        # Rectangle
        if (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (abs(e1 - e3) <= 0.03 * np.mean([e1, e3, e5])) and \
                (abs(e4 - e5) <= 0.03 * np.mean([e1, e3, e5])) and \
                ((e2 < e4 and e2 < e1 and e5 > e3) or (e2 > e4 and e2 > e1 and e5 < e3)):
            patterns['Rectangle'].append((window.index[0], window.index[-1]))

        # Double_Top
        if (e2 > e1) and (e2 > e3) and (e4 > e3) and (e4 > e5) and \
                (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (abs(e1 - e3) <= 0.03 * np.mean([e1, e3, e5])) and \
                (abs(e4 - e5) <= 0.03 * np.mean([e1, e3, e5])):
            patterns['Double_Top'].append((window.index[0], window.index[-1]))

        # Double_Bottom
        if (e2 < e1) and (e2 < e3) and (e4 < e3) and (e4 < e5) and \
                (abs(e2 - e4) <= 0.03 * np.mean([e1, e3, e5])) and \
                (abs(e1 - e3) <= 0.03 * np.mean([e1, e3, e5])) and \
                (abs(e4 - e5) <= 0.03 * np.mean([e1, e3, e5])):
            patterns['Double_Bottom'].append((window.index[0], window.index[-1]))

        # Diamond_Top
        if (e2 < e1) and (e2 < e3) and (e4 < e3) and (e4 < e5) and \
                (abs(e2 - e4) >= 0.7 * np.mean([e1, e3, e5])) and \
                (abs(e1 - e3) <= 0.03 * np.mean([e1, e3, e5])) and \
                (abs(e4 - e5) <= 0.03 * np.mean([e1, e3, e5])):
            patterns['Diamond_Top'].append((window.index[0], window.index[-1]))

        # Falling_Wedge
        if (e2 > e1) and (e2 > e3) and (e4 > e3) and (e4 > e5) and \
                (e1 - e2 >= 0.15 * np.mean([e1, e3, e5])) and \
                (e1 - e2 <= 0.618 * (e1 - e3)) and \
                (e4 - e5 >= 0.15 * np.mean([e1, e3, e5])) and \
                (e4 - e5 <= 0.618 * (e1 - e3)):
            patterns['Falling_Wedge'].append((window.index[0], window.index[-1]))

        # Rising_Wedge
        if (e2 < e1) and (e2 < e3) and (e4 < e3) and (e4 < e5) and \
                (e2 - e1 >= 0.15 * np.mean([e1, e3, e5])) and \
                (e2 - e1 <= 0.618 * (e3 - e1)) and \
                (e5 - e4 >= 0.15 * np.mean([e1, e3, e5])) and \
                (e5 - e4 <= 0.618 * (e3 - e1)):
            patterns['Rising_Wedge'].append((window.index[0], window.index[-1]))

        # Rounding_Bottom
        if (e5 > e4) and (e4 > e3) and (e3 > e2) and (e2 > e1) and \
                (e1 < np.mean([e2, e5])) and (e5 - e1 >= 0.1 * np.mean([e1, e5])) and \
                (abs((e1 - np.min([e2, e3, e4, e5])) / (e5 - np.min([e2, e3, e4, e5]))) <= 0.15):
            patterns['Rounding_Bottom'].append((window.index[0], window.index[-1]))

        # Triple_Top
        if (e1 > e2) and (e2 < e3) and (e3 > e4) and (e4 < e5) and \
                (e1 - np.min([e2, e3, e4]) >= 0.05 * np.mean([e1, e2, e3, e4, e5])) and \
                (e1 - e2 <= 0.05 * np.mean([e1, e2, e3, e4, e5])) and \
                (e3 - e2 <= 0.05 * np.mean([e1, e2, e3, e4, e5])) and \
                (e3 - e4 <= 0.05 * np.mean([e1, e2, e3, e4, e5])):
            patterns['Triple_Top'].append((window.index[0], window.index[-1]))

        # Triple_Bottom
        if (e1 < e2) and (e2 > e3) and (e3 < e4) and (e4 > e5) and \
                (np.max([e2, e3, e4]) - e1 >= 0.05 * np.mean([e1, e2, e3, e4, e5])) and \
                (e2 - e1 <= 0.05 * np.mean([e1, e2, e3, e4, e5])) and \
                (e3 - e2 <= 0.05 * np.mean([e1, e2, e3, e4, e5])) and \
                (e4 - e3 <= 0.05 * np.mean([e1, e2, e3, e4, e5])):
            patterns['Triple_Bottom'].append((window.index[0], window.index[-1]))

    return patterns

pattern_ranking = {
 'Head_and_Shoulders': 1,
 'Bullish_Flag': 2,
 'Bearish_Flag': 2,
 'Ascending_Triangle': 3,
 'Descending_Triangle': 3,
 'Bullish_Channel': 4,
 'Bearish_Channel': 4,
 'Symmetrical_Triangle': 5,
 'Rectangle': 6,
 'Double_Top': 7,
 'Double_Bottom': 7,
 'Bullish_Pennant': 8,
 'Bearish_Pennant': 8,
 'Rounding_Bottom': 9,
 'Diamond_Top': 10,
 'Falling_Wedge': 11,
 'Rising_Wedge': 11,
 'Inverse_Head_and_Shoulders': 12,
 'Horizontal_Channel': 13,
 'Triple_Top': 14,
 'Triple_Bottom': 14,
 'Cup_with_Handle': 15,

}


def get_best_pattern(ticker,start_date):
    # create a dictionary to store the best pattern for each range
    best_patterns = {}
    df1 = get_data(ticker,start_date)
    patterns =  find_patterns(ticker,start_date)

    # loop through the patterns
    for pattern, ranges in patterns.items():
        # loop through the ranges for this pattern
        for start, end in ranges:
            # if this is the first pattern for this range, add it to the dictionary
            if (start, end) not in best_patterns:
                # extract the start and end index values from df1 using iloc
                start_index = df1.iloc[start].name
                end_index = df1.iloc[end].name
                best_patterns[(start_index, end_index)] = (pattern, pattern_ranking[pattern])
            else:
                # if there is already a pattern for this range, compare the rankings
                current_ranking = pattern_ranking[best_patterns[(start, end)][0]]
                new_ranking = pattern_ranking[pattern]
                if new_ranking < current_ranking:
                    # if this pattern has a higher ranking, replace the current best pattern
                    # extract the start and end index values from df1 using iloc
                    start_index = df1.iloc[start].name
                    end_index = df1.iloc[end].name
                    best_patterns[(start_index, end_index)] = (pattern, new_ranking)

    # return a list of the best patterns for each range
    return [(pattern, start, end) for (start, end), (pattern, ranking) in best_patterns.items()]


if __name__ == '__main__':
    a = get_best_pattern('LT.NS', '2020-01-01')
    print(a)