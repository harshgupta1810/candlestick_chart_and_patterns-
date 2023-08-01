import pandas as pd
from reconise_pattern import get_data, get_best_pattern
def head_and_shoulders(df):

    # Find the highest high and lowest low in the first and third peaks
    first_peak_high = df.iloc[:df.shape[0]//3]['Close'].max()
    first_peak_low = df.iloc[:df.shape[0]//3]['Close'].min()
    third_peak_high = df.iloc[df.shape[0]//3*2:]['Close'].max()
    third_peak_low = df.iloc[df.shape[0]//3*2:]['Close'].min()

    # Find the neckline by connecting the lows of the first and third peaks
    neckline = df[(df['Close'] == first_peak_low) | (df['Close'] == third_peak_low)]

    # Find the distance between the neckline and the highest high of the pattern
    distance = abs(first_peak_high - neckline.iloc[0]['Close'])

    # Calculate the target and stoploss levels
    target = third_peak_low - distance
    stoploss = first_peak_high

    return target, stoploss

def bullish_flag(df):
    # Calculate the flagpole height
    flagpole = df['Close'].max() - df['Close'].min()

    # Calculate the breakout level
    breakout = df['Close'].max()

    # Calculate the target level
    target = breakout + flagpole

    # Calculate the stop-loss level
    stop_loss = df['Close'].min()

    # Return the target and stop-loss levels
    return target, stop_loss

def bearish_flag(df):
    # Calculate the flagpole height
    flagpole = df['Close'].max() - df['Close'].min()

    # Calculate the breakout level
    breakout = df['Close'].min()

    # Calculate the target level
    target = breakout - flagpole

    # Calculate the stop-loss level
    stop_loss = df['Close'].max()

    # Return the target and stop-loss levels
    return target, stop_loss

def ascending_triangle(df):
    # Calculate the support and resistance levels
    support = df['Close'].max()
    resistance = df['Close'].min()

    # Calculate the pattern height
    pattern_height = support - resistance

    # Calculate the target level
    target = resistance + pattern_height

    # Calculate the stop-loss level
    stop_loss = support - pattern_height

    # Return the target and stop-loss levels
    return target, stop_loss

def descending_triangle(df):
    # Calculate the support and resistance levels
    support = df['Close'].min()
    resistance = df['Close'].min()

    # Calculate the pattern height
    pattern_height = resistance - support

    # Calculate the target level
    target = support - pattern_height

    # Calculate the stop-loss level
    stop_loss = resistance + pattern_height

    # Return the target and stop-loss levels
    return target, stop_loss

def bullish_channel(df):
    # Find the highest high and lowest low in the first and second touches
    first_touch_high = df.iloc[:df.shape[0]//2]['Close'].max()
    first_touch_low = df.iloc[:df.shape[0]//2]['Close'].min()
    second_touch_high = df.iloc[df.shape[0]//2:]['Close'].max()
    second_touch_low = df.iloc[df.shape[0]//2:]['Close'].min()

    # Find the slope of the channel
    slope = (second_touch_high - first_touch_high) / (df.shape[0]//2)

    # Find the distance between the first touch and the channel
    distance = abs(first_touch_high - first_touch_low)

    # Calculate the target and stoploss levels
    target = second_touch_high + distance
    stoploss = first_touch_low - distance

    return target, stoploss

def bearish_channel(df):
    # Find the highest high and lowest low in the first and second touches
    first_touch_high = df.iloc[:df.shape[0]//2]['Close'].max()
    first_touch_low = df.iloc[:df.shape[0]//2]['Close'].min()
    second_touch_high = df.iloc[df.shape[0]//2:]['Close'].max()
    second_touch_low = df.iloc[df.shape[0]//2:]['Close'].min()

    # Find the slope of the channel
    slope = (second_touch_low - first_touch_low) / (df.shape[0]//2)

    # Find the distance between the first touch and the channel
    distance = abs(first_touch_high - first_touch_low)

    # Calculate the target and stoploss levels
    target = second_touch_low - distance
    stoploss = first_touch_high + distance

    return target, stoploss

def symmetrical_triangle(df):
    # Find the highest high and lowest low in the first and second touches
    first_touch_high = df.iloc[:df.shape[0]//2]['Close'].max()
    first_touch_low = df.iloc[:df.shape[0]//2]['Close'].min()
    second_touch_high = df.iloc[df.shape[0]//2:]['Close'].max()
    second_touch_low = df.iloc[df.shape[0]//2:]['Close'].min()

    # Find the distance between the first touch and the apex of the triangle
    distance = abs(first_touch_high - first_touch_low)

    # Calculate the target and stoploss levels
    if first_touch_high < second_touch_high:
        target = second_touch_high + distance
        stoploss = first_touch_low - distance
    else:
        target = second_touch_low - distance
        stoploss = first_touch_high + distance

    return target, stoploss

def rectangle(df):
    # Find the highest high and lowest low in the range
    high = df['Close'].max()
    low = df['Close'].min()

    # Find the distance between the high and the low
    distance = abs(high - low)

    # Calculate the target and stoploss levels
    target = high + distance
    stoploss = low - distance

    return target, stoploss

def double_top(df):
    # Find the highest high in the first and second tops
    first_top_high = df.iloc[:df.shape[0]//2]['Close'].max()
    second_top_high = df.iloc[df.shape[0]//2:]['Close'].max()

    # Find the lowest low in the valley
    valley_low = df.iloc[df.shape[0]//4:3*df.shape[0]//4]['Close'].min()

    # Find the distance between the valley and the first top
    distance = abs(first_top_high - valley_low)

    # Calculate the target and stoploss levels
    target = second_top_high + distance
    stoploss = valley_low - distance

    return target, stoploss

def double_bottom(df):
    # Find the lowest low in the first and second bottoms
    first_bottom_low = df.iloc[:df.shape[0]//2]['Close'].min()
    second_bottom_low = df.iloc[df.shape[0]//2:]['Close'].min()

    # Find the highest high in the valley
    valley_high = df.iloc[df.shape[0]//4:3*df.shape[0]//4]['Close'].max()

    # Find the distance between the valley and the first bottom
    distance = abs(first_bottom_low - valley_high)

    # Calculate the target and stoploss levels
    target = second_bottom_low - distance
    stoploss = valley_high + distance

    return target, stoploss

def bullish_pennant(df):
    # Calculate the height of the pennant flagpole
    flagpole_height = df["Close"].iloc[-1] - df["Close"].iloc[0]

    # Calculate the breakout level (i.e., the top of the pennant)
    breakout_level = df["Close"].max()

    # Calculate the target level
    target = breakout_level + flagpole_height

    # Calculate the stop loss level (i.e., the bottom of the pennant)
    stop_loss = df["Close"].min()

    return (target, stop_loss)

def bearish_pennant(df):
    # Calculate the height of the pennant flagpole
    flagpole_height = df["Close"].iloc[-1] - df["Close"].iloc[0]

    # Calculate the breakout level (i.e., the top of the pennant)
    breakout_level = df["Close"].max()

    # Calculate the target level
    target = breakout_level - flagpole_height

    # Calculate the stop loss level (i.e., the bottom of the pennant)
    stop_loss = df["Close"].max()

    return (target, stop_loss)

def rounding_bottom(df):
    # Calculate the minimum price and its index
    min_price = df['Close'].min()
    min_idx = df['Close'].idxmin()

    # Calculate the left and right sides of the pattern
    left_side = df.loc[:min_idx, 'Close']
    right_side = df.loc[min_idx:, 'Close']

    # Calculate the resistance level
    resistance = min_price + (left_side.max() - min_price) * 0.5

    # Calculate the target and stoploss levels
    target = resistance + (resistance - min_price)
    stoploss = min_price - (left_side.max() - min_price)

    return target, stoploss

def diamond_top(df):
    # Calculate the length of the pattern
    length = len(df)

    # Calculate the midpoint index
    midpoint = length // 2

    # Calculate the left and right sides of the pattern
    left_side = df.iloc[:midpoint, df.columns.get_loc('Close')]
    right_side = df.iloc[midpoint:, df.columns.get_loc('Close')]

    # Calculate the resistance and support levels
    resistance = left_side.max()
    support = right_side.min()

    # Calculate the target and stoploss levels
    target = support - (resistance - support)
    stoploss = resistance + (resistance - support)

    return target, stoploss

def falling_wedge(df):
    # Calculate the length of the pattern
    length = len(df)

    # Calculate the midpoint index
    midpoint = length // 2

    # Calculate the left and right sides of the pattern
    left_side = df.loc[:df.index[midpoint], 'Close']
    right_side = df.loc[df.index[midpoint]:, 'Close']

    # Calculate the resistance and support trendlines
    resistance = left_side.max()
    support = right_side.min()

    # Calculate the target and stoploss levels
    target = resistance - (resistance - support) * 2
    stoploss = support - (resistance - support) * 0.5

    return target, stoploss

def rising_wedge(df):
    # Calculate the length of the pattern
    length = len(df)

    # Calculate the midpoint index
    midpoint = length // 2

    # Calculate the left and right sides of the pattern
    left_side = df.loc[:df.index[midpoint], 'Close']
    right_side = df.loc[df.index[midpoint]:, 'Close']

    # Calculate the resistance and support trendlines
    resistance = right_side.min()
    support = left_side.max()

    # Calculate the target and stoploss levels
    target = support - (resistance - support) * 0.5
    stoploss = resistance - (resistance - support) * 2

    return target, stoploss

def Inverse_Head_and_Shoulders(df):
    # Find the lowest price in the left shoulder
    left_shoulder_low = df.iloc[:round(len(df)/3)]['Close'].min()

    # Find the lowest price in the head
    head_low = df.iloc[round(len(df)/3):round(len(df)*2/3)]['Close'].min()

    # Find the lowest price in the right shoulder
    right_shoulder_low = df.iloc[round(len(df)*2/3):]['Close'].min()

    # Calculate the target price as the distance from the head to the neckline, added to the neckline
    target_price = head_low + (head_low - left_shoulder_low)

    # Calculate the stop loss as the distance from the head to the neckline, subtracted from the neckline
    stop_loss = right_shoulder_low - (head_low - left_shoulder_low)

    return target_price, stop_loss

def Horizontal_Channel(df):
    # Find the highest and lowest prices in the channel
    channel_high = df['Close'].max()
    channel_low = df['Close'].min()

    # Calculate the target price as the distance from the channel high to the channel low, added to the channel high
    target_price = channel_high + (channel_high - channel_low)

    # Calculate the stop loss as the distance from the channel high to the channel low, subtracted from the channel low
    stop_loss = channel_low - (channel_high - channel_low)

    return (target_price, stop_loss)

def Triple_Top(df):
    # Find the highest price in the first top
    first_top_high = df.iloc[:round(len(df)/3)]['Close'].max()

    # Find the highest price in the second top
    second_top_high = df.iloc[round(len(df)/3):round(len(df)*2/3)]['Close'].max()

    # Find the highest price in the third top
    third_top_high = df.iloc[round(len(df)*2/3):]['Close'].max()

    # Calculate the target price as the distance from the triple top high to the neckline, subtracted from the neckline
    target_price = df.iloc[round(len(df)*2/3):]['Close'].min() - (third_top_high - df.iloc[round(len(df)*2/3):]['Close'].min())

    # Calculate the stop loss as the distance from the first top high to the neckline, added to the neckline
    stop_loss = df.iloc[:round(len(df)/3)]['Close'].min() + (first_top_high - df.iloc[:round(len(df)/3)]['Close'].min())

    return (target_price, stop_loss)

def Triple_Bottom(df):
    # Find the lowest price in the first bottom
    first_bottom_low = df.iloc[:round(len(df)/3)]['Close'].min()

    # Find the lowest price in the second bottom
    second_bottom_low = df.iloc[round(len(df)/3):round(len(df)*2/3)]['Close'].min()

    # Find the lowest price in the third bottom
    third_bottom_low = df.iloc[round(len(df)*2/3):]['Close'].min()

    # Calculate the target price as the distance from the triple bottom low to the neckline, added to the neckline
    target_price = df.iloc[round(len(df)*2/3):]['Close'].max() + (df.iloc[round(len(df)*2/3):]['Close'].max() - third_bottom_low)

    # Calculate the stop loss as the distance from the first bottom low to the neckline, subtracted from the neckline
    stop_loss = df.iloc[:round(len(df)/3)]['Close'].max() - (first_bottom_low - df.iloc[:round(len(df)/3)]['Close'].max())

    return (target_price, stop_loss)

def Cup_with_Handle(df):
    # Find the highest price in the cup
    cup_high = df.iloc[:round(len(df)*0.7)]['Close'].max()

    # Find the lowest price in the handle
    handle_low = df.iloc[round(len(df)*0.7):]['Close'].min()

    # Calculate the target price as the distance from the cup high to the breakout point, added to the breakout point
    target_price = handle_low + (cup_high - handle_low)

    # Calculate the stop loss as the distance from the cup high to the handle low, subtracted from the handle low
    stop_loss = handle_low - (cup_high - handle_low)

    return (target_price, stop_loss)

def calculate_target_stoploss(df,patterns):
    result = []
    for pattern in patterns:
        name, start, end = pattern

        df2 = df.loc[start:end].copy()
        df2.index = pd.to_datetime(df2.index)
        # Convert the 'Close' column to a numeric data type using .loc
        df2['Close'] = pd.to_numeric(df2['Close'], errors='coerce')

        # Calculate the target and stop loss for the Bullish Flag pattern
        target, stop_loss = Cup_with_Handle(df)

        if name == 'Head_and_Shoulders':
            target,stop_loss = head_and_shoulders(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Bullish_Flag':
            target,stop_loss = bullish_flag(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Bearish_Flag':
            target,stop_loss = bearish_flag(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Ascending_Triangle':
            target,stop_loss = ascending_triangle(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Descending_Triangle':
            target,stop_loss = descending_triangle(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Bullish_Channel':
            target,stop_loss = bullish_channel(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Bearish_Channel' :
            target,stop_loss = bearish_channel(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Symmetrical_Triangle':
            target,stop_loss = symmetrical_triangle(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Rectangle':
            target,stop_loss = rectangle(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Double_Top' :
            target,stop_loss = double_top(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Double_Bottom':
            target,stop_loss = double_bottom(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Bullish_Pennant' :
            target,stop_loss = bullish_pennant(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Bearish_Pennant':
            target,stop_loss = bearish_pennant(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Rounding_Bottom' :
            target,stop_loss = rounding_bottom(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Diamond_Top':
            target,stop_loss = diamond_top(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Falling_Wedge' :
            target,stop_loss = falling_wedge(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Rising_Wedge' :
            target,stop_loss = rising_wedge(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Inverse_Head_and_Shoulders' :
            target,stop_loss = Inverse_Head_and_Shoulders(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Horizontal_Channel' :
            target,stop_loss = Horizontal_Channel(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Triple_Top':
            target,stop_loss = Triple_Top(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Triple_Bottom' :
            target,stop_loss = Triple_Bottom(df2)
            result.append((name, start,end,target, stop_loss))

        elif name == 'Cup_with_Handle':
            target,stop_loss = Cup_with_Handle(df2)
            result.append((name, start,end,target, stop_loss))



        else:
            # For other patterns, set the target and stop loss to None
            target = None
            stop_loss = None
            result.append((name, start,end,target, stop_loss))

        # Add a check to make sure that target and stop_loss are not None

        #result.append((name, start,end,target, stop_loss))


    return pd.DataFrame(result, columns=['Pattern', 'formation_date','breakout_date','Target', 'Stop Loss'])

if __name__ == '__main__':
    df = get_data('LT.NS','2020-01-01')
    b= get_best_pattern('LT.NS','2020-01-01')
    c =  calculate_target_stoploss(df,b)
    print(c)