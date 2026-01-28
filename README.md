# Binance Trading Bot (Botik)

A Python-based trading bot for Binance Futures, implementing a customizable strategy based on **Parabolic SAR**, **Volume Filtering**, and **Price Channel Breakouts**.

## Features

*   **Strategy**:
    *   **Entry**: Parabolic SAR Reversals + Optional Volume/Ticks Filter.
    *   **Exit**: Price Channel Breakout (Lowest Low/Highest High).
*   **Backtesting**: Built-in script to verify strategy performance on historical data with detailed statistics and visualization.
*   **Visualization**: Charts trades, indicators, and PnL on historical data.
*   **Safety**: Uses Binance Testnet by default.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd botik
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Environment Variables**:
    Create a `.env` file in the root directory:
    ```env
    BINANCE_API_KEY=your_testnet_api_key
    BINANCE_API_SECRET=your_testnet_api_secret
    ```
    *Note: Get your keys from the [Binance Testnet](https://testnet.binancefuture.com/en/login).*

2.  **Strategy Settings**:
    Edit `config.py` to adjust parameters:
    *   `SYMBOL`: Trading pair (e.g., "BTCUSDT").
    *   `INTERVAL`: Candle timeframe (e.g., "5m").
    *   `SAR_STEP`, `SAR_MAX`: Parabolic SAR settings.
    *   `ENABLE_VOLUME_FILTER`: 1 (Volume), 2 (Num Trades), 0 (Disable).
    *   `TRAIL_STOP_LENGTH_LX/SX`: Lookback period for Price Channel exits.

## Usage

### Run Live Signal Check
To check the current market signal:
```bash
python3 main.py
```
This prints the latest signal (`BUY`, `SELL`, `HOLD`, `EXIT...`) based on the most recent completed candle.

### Run Backtest
To test the strategy on historical data:
```bash
python3 test_strategy.py
```
The script will prompt for:
1.  **Days to backtest**: Date range to fetch.
2.  **Show trade details?**: Prints every trade entry/exit.
3.  **Show plot?**: Opens a graphical chart of the backtest.

## Project Structure

*   `main.py`: Entry point for live execution.
*   `strategy.py`: Core logic for signal generation.
*   `indicators.py`: Custom indicator calculations (Parabolic SAR, Volume MA, etc.).
*   `data.py`: Binance API data fetching.
*   `config.py`: Configuration constants.
*   `test_strategy.py`: Backtesting and verification tool.

## Disclaimer
This software is for educational purposes only. Use at your own risk. Start with Testnet before using real funds.
