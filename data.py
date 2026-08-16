from binance.client import Client
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

client = Client(api_key, api_secret)

def get_klines(symbol, interval, limit=365):
    klines = client.futures_klines(
        symbol=symbol,
        interval=interval,
        limit=limit
    )

    df = pd.DataFrame(klines, columns=[
        "time","open","high","low","close","volume",
        "close_time","qav","num_trades",
        "taker_base_vol","taker_quote_vol","ignore"
    ])

    for col in ["open","high","low","close","volume"]:
        df[col] = df[col].astype(float)

    return df


def get_historical_klines_by_days(symbol, interval, days_back, use_cache=True, force_update=False):
    cache_dir = "data_cache"
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        
    # Create a safe filename
    safe_symbol = symbol.replace("/", "")
    filename = os.path.join(cache_dir, f"{safe_symbol}_{interval}_{days_back}d.csv")
    
    # Try to load from cache
    if use_cache and not force_update and os.path.exists(filename):
        print(f"Loading data from cache: {filename}")
        try:
            df = pd.read_csv(filename)
            # Ensure proper types
            # Convert close_time back to int/datetime if needed, though primarily we need float cols
            # But the original code didn't parse dates? Ah, pd.read_csv might infer or keep as object/int
            # Let's ensure float columns are floats
            for col in ["open","high","low","close","volume","num_trades"]:
                df[col] = df[col].astype(float)
            return df
        except Exception as e:
            print(f"Error loading cache: {e}. Fetching fresh data.")

    print(f"Fetching fresh data for {symbol} ({days_back} days)...")
    start_str = f"{days_back} days ago UTC"
    klines = client.get_historical_klines(symbol, interval, start_str)
    
    df = pd.DataFrame(klines, columns=[
        "time","open","high","low","close","volume",
        "close_time","qav","num_trades",
        "taker_base_vol","taker_quote_vol","ignore"
    ])
    
    for col in ["open","high","low","close","volume","num_trades"]:
        df[col] = df[col].astype(float)
        
    # Save to cache
    if use_cache:
        print(f"Saving data to cache: {filename}")
        df.to_csv(filename, index=False)
        
    return df
