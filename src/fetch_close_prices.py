import yfinance as yf
import pandas as pd

def fetch_close_prices(tickers, period):
    """
    Fetch close prices for the given tickers and period.

    Args:
        tickers (list): A list of stock tickers.
        period (str): Time period for fetching the close prices.

    Returns:
        pandas.DataFrame: A DataFrame containing the close prices.
    """
    tickers_str = [str(tick) for tick in tickers]
    data = yf.download(tickers_str, period=period)['Close'].reset_index()

    return data