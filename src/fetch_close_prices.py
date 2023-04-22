import yaml
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
    config = {'tickers': tickers, 'period': period}

    with open('config.yaml', 'w') as file:
        yaml.dump(config, file)

    data = yf.download(tickers, period='1d')['Close'].reset_index()

    return data