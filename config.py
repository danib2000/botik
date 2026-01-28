SYMBOL = "BTCUSDT"
INTERVAL = "5m"

SAR_STEP = 0.02
SAR_MAX = 0.2

# Strategy Parameters
ENABLE_VOLUME_FILTER = 1  # 1: Volume, 2: Ticks (Num Trades)
ENABLE_PRICE_CHANNEL = 1
ENABLE_STOPLOSS = 0
ENABLE_PROFITTGT = 0
ENABLE_TRAILING = 0

VOLUME_AVG_LENGTH = 20
TRAIL_STOP_LENGTH_LX = 20  # Lowest Low lookup for Long Exit
TRAIL_STOP_LENGTH_SX = 20  # Highest High lookup for Short Exit

# Exit Parameters (Percentages)
C_STOPLOSS = 1.0
C_PROFITTGT = 2.0
C_TRAILSTOP_THD = 1.0  # Activation threshold
C_TRAILSTOP = 1.0      # Trailing percent
