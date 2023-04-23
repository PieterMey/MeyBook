from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['yfinance', 'yaml', 'os'],
    'includes': ['tkinter', 'pandas', 'numpy', 'custom_entry', 'fetch_close_prices', 'utils'],
    'iconfile': 'images/app_icon.icns'
}

setup(
    app=APP,
    name='StockClosePrices',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)