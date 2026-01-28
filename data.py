from binance.client import Client
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

client = Client(api_key, api_secret, testnet=True)

def get_klines(symbol, interval, limit=200):
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

    return df


def get_historical_klines_by_days(symbol, interval, days_back):
    start_str = f"{days_back} days ago UTC"
    klines = client.get_historical_klines(symbol, interval, start_str)
    
    df = pd.DataFrame(klines, columns=[
        "time","open","high","low","close","volume",
        "close_time","qav","num_trades",
        "taker_base_vol","taker_quote_vol","ignore"
    ])
    
    for col in ["open","high","low","close","volume","num_trades"]:
        df[col] = df[col].astype(float)
        
    return df
