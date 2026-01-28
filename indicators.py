import pandas as pd

def add_sar(df, step, max_step):
    """
    Calculates Parabolic SAR manually to ensure correctness.
    Matches standard logic:
    - SAR follows price.
    - Accelerates on new highs/lows.
    - Reverses when price breaches SAR.
    """
    high = df['high'].values
    low = df['low'].values
    close = df['close'].values
    
    # Initialize output arrays
    sar = [0.0] * len(df)
    sar_dir = [0] * len(df) # 1 for Long, -1 for Short
    
    # Initial Trend Assumption (start at index 1)
    # Assume Long if Close > Open, else Short? Or use first bar range?
    # Simple start: Trend Long, SAR = Low[0], EP = High[0], AF = step
    
    trend = 1 # 1 Long, -1 Short
    sar[0] = low[0]
    ep = high[0] # Extreme Point
    af = step
    
    # Loop efficiently
    for i in range(1, len(df)):
        prev_sar = sar[i-1]
        
        # Calculate tentative SAR
        new_sar = prev_sar + af * (ep - prev_sar)
        
        # Constraints
        if trend == 1: # Uptrend
            # SAR cannot be higher than previous 2 lows
            prev_low = low[i-1]
            prev2_low = low[i-2] if i >= 2 else low[i-1]
            new_sar = min(new_sar, prev_low, prev2_low)
            
            # Check Reversal
            if low[i] < new_sar:
                trend = -1
                sar[i] = ep # SAR becomes the extreme high of the previous move
                ep = low[i] # Reset EP to current low
                af = step # Reset AF
            else:
                sar[i] = new_sar
                # Update EP and AF
                if high[i] > ep:
                    ep = high[i]
                    af = min(af + step, max_step)
                    
        else: # Downtrend
            # SAR cannot be lower than previous 2 highs
            prev_high = high[i-1]
            prev2_high = high[i-2] if i >= 2 else high[i-1]
            new_sar = max(new_sar, prev_high, prev2_high)
            
            # Check Reversal
            if high[i] > new_sar:
                trend = 1
                sar[i] = ep # SAR becomes the extreme low of the previous move
                ep = high[i] # Reset EP to current high
                af = step
            else:
                sar[i] = new_sar
                # Update EP and AF
                if low[i] < ep:
                    ep = low[i]
                    af = min(af + step, max_step)
                    
        sar_dir[i] = trend
        
    df["sar"] = sar
    df["sar_dir"] = sar_dir
    
    return df


def add_volume_average(df, length):
    # Use standard pandas rolling mean
    df["vol_avg"] = df["volume"].rolling(window=length).mean()
    df["num_trades_avg"] = df["num_trades"].rolling(window=length).mean()
    return df


def add_price_channel(df, length_lx, length_sx):
    # Lowest Low for Long Exit (LX) - needs to look at previous bars
    # Using shift(1) to match "Lowest(Low, Length)[1]" logic - previous bar's lowest
    
    df["lowest_low"] = df["low"].rolling(window=length_lx).min()
    df["highest_high"] = df["high"].rolling(window=length_sx).max()
    
    # Shift them by 1 to represent [1] - value as of previous bar
    df["lowest_low_prev"] = df["lowest_low"].shift(1)
    df["highest_high_prev"] = df["highest_high"].shift(1)
    
    return df

