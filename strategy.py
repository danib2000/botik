import pandas as pd
import config

def _check_volume_filter(row: pd.Series, p_enable_vol: int) -> bool:
    """Helper function to evaluate volume conditions."""
    if p_enable_vol == 0:
        return True
    
    if p_enable_vol == 1:
        # Volume > Average Volume
        return row["volume"] > row["vol_avg"]
    elif p_enable_vol == 2:
        # Ticks (Num Trades) > Average
        return row["num_trades"] > row["num_trades_avg"]
        
    return False

def check_buy_signal(row: pd.Series, prev_row: pd.Series, params: dict = None) -> bool:
    """
    Checks for Buy Entry Signal
    """
    params = params or {}
    p_enable_vol = params.get("ENABLE_VOLUME_FILTER", config.ENABLE_VOLUME_FILTER)

    # 1. Parabolic SAR Reversal (Bearish to Bullish)
    # Note: sar_dir 1 is bullish (price > sar), -1 is bearish
    sar_reversal_buy = (prev_row["sar_dir"] == -1) and (row["sar_dir"] == 1)

    if not sar_reversal_buy:
        return False
        
    # 2. Volume Filter
    return _check_volume_filter(row, p_enable_vol)


def check_sell_short_signal(row: pd.Series, prev_row: pd.Series, params: dict = None) -> bool:
    """
    Checks for Sell Short Entry Signal
    """
    params = params or {}
    p_enable_vol = params.get("ENABLE_VOLUME_FILTER", config.ENABLE_VOLUME_FILTER)

    # 1. Parabolic SAR Reversal (Bullish to Bearish)
    sar_reversal_sell = (prev_row["sar_dir"] == 1) and (row["sar_dir"] == -1)
    
    if not sar_reversal_sell:
        return False
        
    # 2. Volume Filter
    return _check_volume_filter(row, p_enable_vol)


def check_exit_signal(row: pd.Series, position: int, params: dict = None):
    """
    Checks for Exit Signals based on Price Channel.
    position: 1 for Long, -1 for Short, 0 for None
    """
    params = params or {}
    p_enable_pc = params.get("ENABLE_PRICE_CHANNEL", config.ENABLE_PRICE_CHANNEL)

    if p_enable_pc == 0:
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


def get_signal(df: pd.DataFrame, params: dict = None) -> str:
    """
    Determines the signal for the last completed candle.
    """
    if len(df) < 2:
        return "HOLD"
        
    curr = df.iloc[-1]
    prev = df.iloc[-2]
    
    # Check Entries
    if check_buy_signal(curr, prev, params):
        return "BUY"
    
    if check_sell_short_signal(curr, prev, params):
        return "SELL_SHORT"
        
    # Check Exits
    exit_long = check_exit_signal(curr, 1, params)
    if exit_long:
        return "EXIT_LONG_IF_HELD"
        
    exit_short = check_exit_signal(curr, -1, params)
    if exit_short:
        return "EXIT_SHORT_IF_HELD"
        
    return "HOLD"
