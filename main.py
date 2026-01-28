from config import *
from data import get_klines
from indicators import add_sar, add_volume_average, add_price_channel
from strategy import get_signal

def run():
    df = get_klines(SYMBOL, INTERVAL)
    df = add_sar(df, SAR_STEP, SAR_MAX)
    df = add_volume_average(df, VOLUME_AVG_LENGTH)
    df = add_price_channel(df, TRAIL_STOP_LENGTH_LX, TRAIL_STOP_LENGTH_SX)

    signal = get_signal(df)
    price = df["close"].iloc[-1]

    print(f"{SYMBOL} | {INTERVAL} | {price} | {signal}")

if __name__ == "__main__":
    run()

