import config
from data import get_klines
from indicators import add_sar, add_volume_average, add_price_channel
from strategy import get_signal

def run():
    df = get_klines(config.SYMBOL, config.INTERVAL)
    df = add_sar(df, config.SAR_STEP, config.SAR_MAX)
    df = add_volume_average(df, config.VOLUME_AVG_LENGTH)
    df = add_price_channel(df, config.TRAIL_STOP_LENGTH_LX, config.TRAIL_STOP_LENGTH_SX)

    signal = get_signal(df)
    price = df["close"].iloc[-1]

    print(f"{config.SYMBOL} | {config.INTERVAL} | {price} | {signal}")

if __name__ == "__main__":
    run()
