import yfinance as yf

# Define the tickers you want to get the close price for
tickers = ['AAPL', 'GOOGL', 'MSFT']

# Define the period for which you want the close price data (e.g., '1d', '5d', '1mo', '1y', '5y', 'max')
period = '1d'

# Fetch the data
data = yf.download(tickers, period=period)

# Extract the close prices
close_prices = data['Close']

# Print the close prices
print(close_prices)