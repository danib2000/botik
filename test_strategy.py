import pandas as pd
import sys
import matplotlib.pyplot as plt
from config import *
from data import get_historical_klines_by_days
from indicators import add_sar, add_volume_average, add_price_channel
from strategy import check_buy_signal, check_sell_short_signal, check_exit_signal

def run_backtest(days_back=7, show_trades=False, show_plot=False):
    print(f"Fetching data for {SYMBOL} for last {days_back} days...")
    df = get_historical_klines_by_days(SYMBOL, INTERVAL, days_back)
    
    print(f"Loaded {len(df)} candles.")
    print("Calculating indicators...")
    df = add_sar(df, SAR_STEP, SAR_MAX)
    df = add_volume_average(df, VOLUME_AVG_LENGTH)
    df = add_price_channel(df, TRAIL_STOP_LENGTH_LX, TRAIL_STOP_LENGTH_SX)
    
    print("-" * 60)
    print("Running Backtest Loop...")
    
    trades = []
    current_position = 0 # 0: None, 1: Long, -1: Short
    entry_price = 0
    entry_time = None
    
    # Store indices for plotting
    buy_indices = []
    sell_indices = [] # Short entries
    exit_indices = []
    
    if show_trades:
        print(f"{'Time':<20} | {'Type':<10} | {'Price':<10} | {'PnL %'}")
        print("-" * 60)

    for i in range(50, len(df)):
        current_row = df.iloc[i]
        prev_row = df.iloc[i-1]
        
        timestamp = pd.to_datetime(current_row["close_time"], unit="ms")
        price = current_row["close"]
        
        # Check Exits if in position
        exit_code = None
        if current_position == 1:
            exit_signal = check_exit_signal(current_row, 1)
            if exit_signal:
                exit_code = "EXIT_LONG"
        elif current_position == -1:
            exit_signal = check_exit_signal(current_row, -1)
            if exit_signal:
                exit_code = "EXIT_SHORT"
        
        if current_position != 0 and exit_code:
            pnl = 0
            if current_position == 1:
                pnl = (price - entry_price) / entry_price * 100
                trades.append({"type": "LONG", "entry_price": entry_price, "exit_price": price, "pnl_pct": pnl, "entry_time": entry_time, "exit_time": timestamp})
            elif current_position == -1:
                pnl = (entry_price - price) / entry_price * 100
                trades.append({"type": "SHORT", "entry_price": entry_price, "exit_price": price, "pnl_pct": pnl, "entry_time": entry_time, "exit_time": timestamp})
            
            exit_indices.append((i, price))
            
            if show_trades:
                print(f"{timestamp} | {exit_code:<10} | {price:<10.2f} | {pnl:+.2f}%")
            
            current_position = 0
            entry_price = 0
            continue 

        # Check Entries if not in position
        if current_position == 0:
            if check_buy_signal(current_row, prev_row):
                current_position = 1
                entry_price = price
                entry_time = timestamp
                buy_indices.append((i, price))
                if show_trades:
                    print(f"{timestamp} | {'LONG_ENTRY':<10} | {price:<10.2f} | -")
                
            elif check_sell_short_signal(current_row, prev_row):
                current_position = -1
                entry_price = price
                entry_time = timestamp
                sell_indices.append((i, price))
                if show_trades:
                    print(f"{timestamp} | {'SHRT_ENTRY':<10} | {price:<10.2f} | -")

    # Calculate Stats
    print("-" * 60)
    if not trades:
        print("No trades executed.")
        return

    total_trades = len(trades)
    profitable_trades = [t for t in trades if t["pnl_pct"] > 0]
    losing_trades = [t for t in trades if t["pnl_pct"] <= 0]
    
    total_profit_pct = sum(t["pnl_pct"] for t in profitable_trades)
    total_loss_pct = abs(sum(t["pnl_pct"] for t in losing_trades))
    
    net_profit_pct = sum(t["pnl_pct"] for t in trades)
    percent_profitable = (len(profitable_trades) / total_trades) * 100
    
    profit_factor = total_profit_pct / total_loss_pct if total_loss_pct > 0 else float('inf')
    
    # Drawdown
    cumulative_pnl = 0
    max_pnl = 0
    max_drawdown = 0
    
    for t in trades:
        cumulative_pnl += t["pnl_pct"]
        max_pnl = max(max_pnl, cumulative_pnl)
        drawdown = max_pnl - cumulative_pnl
        max_drawdown = max(max_drawdown, drawdown)

    print(f"Backtest Results ({days_back} Days):")
    print(f"Total Trades: {total_trades}")
    print(f"Net Profit (Sum %): {net_profit_pct:.2f}%")
    print(f"Max Drawdown (%): {max_drawdown:.2f}%")
    print(f"Profit Factor: {profit_factor:.2f}")
    print(f"Percent Profitable: {percent_profitable:.2f}%")
    print("-" * 60)
    
    if show_plot:
        print("Displaying plot...")
        plt.figure(figsize=(14, 7))
        plt.plot(df.index, df["close"], label="Price", color="black", alpha=0.5)
        plt.plot(df.index, df["sar"], label="Parabolic SAR", color="blue", linestyle="dotted")
        
        # Plot Entries
        for idx, price in buy_indices:
            plt.plot(idx, price, marker='^', color='green', markersize=10, label='Buy' if idx == buy_indices[0][0] else "")
        for idx, price in sell_indices:
            plt.plot(idx, price, marker='v', color='red', markersize=10, label='Sell Short' if idx == sell_indices[0][0] else "")
            
        # Plot Exits
        for idx, price in exit_indices:
            plt.plot(idx, price, marker='x', color='purple', markersize=8, label='Exit' if idx == exit_indices[0][0] else "")
            
        plt.title(f"{SYMBOL} Backtest Results - {days_back} Days")
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    try:
        days_input = input("Enter number of days to backtest (default 7): ")
        days = int(days_input) if days_input else 7
        
        show_trades_input = input("Show trade details? (y/n, default n): ").lower()
        show_trades = show_trades_input == 'y'
        
        show_plot_input = input("Show plot? (y/n, default n): ").lower()
        show_plot = show_plot_input == 'y'
        
    except ValueError:
        days = 7
        show_trades = False
        show_plot = False
        
    run_backtest(days, show_trades, show_plot)
