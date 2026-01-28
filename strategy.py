from config import *

def check_buy_signal(row, prev_row):
    """
    Checks for Buy Entry Signal
    """
    # 1. Parabolic SAR Reversal (Bearish to Bullish)
    # Note: sar_dir 1 is bullish (price > sar), -1 is bearish
    sar_reversal_buy = (prev_row["sar_dir"] == -1) and (row["sar_dir"] == 1)

    if not sar_reversal_buy:
        return False
        
    # 2. Volume Filter
    if ENABLE_VOLUME_FILTER == 0:
        return True
    
    vol_condition = False
    if ENABLE_VOLUME_FILTER == 1:
        # Volume > Average Volume
        vol_condition = row["volume"] > row["vol_avg"]
    elif ENABLE_VOLUME_FILTER == 2:
        # Ticks (Num Trades) > Average
        vol_condition = row["num_trades"] > row["num_trades_avg"]
        
    return vol_condition


def check_sell_short_signal(row, prev_row):
    """
    Checks for Sell Short Entry Signal
    """
    # 1. Parabolic SAR Reversal (Bullish to Bearish)
    sar_reversal_sell = (prev_row["sar_dir"] == 1) and (row["sar_dir"] == -1)
    
    if not sar_reversal_sell:
        return False
        
    # 2. Volume Filter
    if ENABLE_VOLUME_FILTER == 0:
        return True
    
    vol_condition = False
    if ENABLE_VOLUME_FILTER == 1:
        vol_condition = row["volume"] > row["vol_avg"]
    elif ENABLE_VOLUME_FILTER == 2:
        vol_condition = row["num_trades"] > row["num_trades_avg"]
        
    return vol_condition


def check_exit_signal(row, position):
    """
    Checks for Exit Signals based on Price Channel.
    position: 1 for Long, -1 for Short, 0 for None
    """
    if ENABLE_PRICE_CHANNEL == 0:
        return False
        
    if position == 1: # Long Position
        # Exit if Low < Lowest Low of previous N bars
        if row["low"] < row["lowest_low_prev"]:
            return "EXIT_LONG"
            
    elif position == -1: # Short Position
        # Exit if High > Highest High of previous N bars
        if row["high"] > row["highest_high_prev"]:
            return "EXIT_SHORT"
            
    return False


def get_signal(df):
    """
    Determines the signal for the last completed candle.
    """
    # Look at the last closed candle (iloc[-1]) and the one before it (iloc[-2])
    # Assuming df contains up-to-date data including the just-closed candle.
    # If the bot runs on "current open candle", we might need iloc[-2] vs [-3].
    # But usually 'get_klines' returns completed candles if queried right, 
    # or the last row is the 'current' unfinished candle.
    # Standard practice: Signal is confirmed on the CLOSE of the bar.
    # So we look at the last COMPLETED bar.
    
    # Let's assume the last row in df is the LATEST candle.
    # If it is incomplete (Binance API returns current open candle as last),
    # we should arguably look at -2 as the 'last confirmed' and -3 as 'prev'.
    # HOWEVER, standard backtesting checks "If Condition on Close".
    # Let's use the last row as "Current Bar" (potentially open) if we want real-time,
    # OR use -2 as "Last Closed Bar" if we want confirmed signals.
    # Safety: Use -2 (Last Closed) and -3 (Prev Closed) to avoid repainting on open candle,
    # OR use -1 if we accept the signal might disappear before close.
    # Decision: Use -1 as "Current Candle" (taking action "next bar at Market" usually implies waiting for close).
    # But wait, logic says "Buy next bar at oParOp stop".
    
    curr = df.iloc[-1]
    prev = df.iloc[-2]
    
    # Check Entries
    if check_buy_signal(curr, prev):
        return "BUY"
    
    if check_sell_short_signal(curr, prev):
        return "SELL_SHORT"
        
    # Check Exits (Requires knowing current position - simplistic stateless version)
    # We can report if an Exit condition is met assuming we WERE in a position
    exit_long = check_exit_signal(curr, 1)
    if exit_long:
        return "EXIT_LONG_IF_HELD"
        
    exit_short = check_exit_signal(curr, -1)
    if exit_short:
        return "EXIT_SHORT_IF_HELD"
        
    return "HOLD"
