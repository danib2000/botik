import pandas as pd
import plotly.graph_objects as go
import mplfinance as mpf
import requests

def get_OHLC(pair, interval, since):

    url = "https://api.kraken.com/0/public/OHLC?pair=" + pair + "&interval=" + interval + "&since=" + since

    payload = {}
    headers = {
       'Accept': 'application/json'
    }

    response = requests.get( url, headers=headers, data=payload)

    return response.json()


# Assuming you have your OHLC data in a pandas DataFrame
# Example of OHLC data structure
kraken_data = get_OHLC("BTCUSDT","60", "1288671200")

ohlc_data = kraken_data["result"]["XBTUSDT"]

# Convert it into a DataFrame
df = pd.DataFrame(ohlc_data, columns=["Timestamp", "Open", "High", "Low", "Close", "VWAP", "Volume", "Count"])

# Convert the timestamp to a datetime format and set it as index
df['Date'] = pd.to_datetime(df['Timestamp'], unit='s')
df.set_index('Date', inplace=True)

# Convert price columns from string to float
df['Open'] = df['Open'].astype(float)
df['High'] = df['High'].astype(float)
df['Low'] = df['Low'].astype(float)
df['Close'] = df['Close'].astype(float)

# Now plot the OHLC data as a candlestick chart
mpf.plot(df[['Open', 'High', 'Low', 'Close']], type='candle', style='charles', title="BTC/USD OHLC Chart", ylabel='Price (USD)')

