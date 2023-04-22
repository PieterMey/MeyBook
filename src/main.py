import yfinance as yf
import yaml
import pandas as pd
import tkinter as tk
from tkinter import filedialog

def fetch_close_prices():
    tickers = [ticker.upper().strip() for ticker in entry_tickers.get().split(',')]
    period = entry_period.get()

    config = {'tickers': tickers, 'period': period}

    with open('config.yaml', 'w') as file:
        yaml.dump(config, file)

    data = yf.download(config['tickers'], period=config['period'])
    close_prices = data['Close']

    output.delete(1.0, tk.END)
    output.insert(tk.END, close_prices)

    global df_close_prices
    df_close_prices = close_prices

def save_to_csv():
    if df_close_prices is not None:
        file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            df_close_prices.transpose().to_csv(file_path)

def clear_tickers_placeholder(event):
    tickers_var.set('')
    entry_tickers.config(fg='black')

def clear_period_placeholder(event):
    period_var.set('')
    entry_period.config(fg='black')

app = tk.Tk()
app.title("Stock Close Prices")

tk.Label(app, text="Tickers (comma separated):").grid(row=0, column=0, sticky=tk.W)
tickers_var = tk.StringVar()
tickers_var.set("e.g. AAPL, GOOGL, MSFT")
entry_tickers = tk.Entry(app, textvariable=tickers_var, fg='grey')
entry_tickers.grid(row=0, column=1)

tk.Label(app, text="Period:").grid(row=1, column=0, sticky=tk.W)
period_var = tk.StringVar()
period_var.set("e.g. 1d, 5d, 1mo, 1yr")
entry_period = tk.Entry(app, textvariable=period_var, fg='grey')
entry_period.grid(row=1, column=1)

fetch_button = tk.Button(app, text="Fetch Close Prices", command=fetch_close_prices)
fetch_button.grid(row=2, column=0)

save_button = tk.Button(app, text="Save to CSV", command=save_to_csv)
save_button.grid(row=2, column=1)

output = tk.Text(app, wrap=tk.WORD)
output.grid(row=3, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

for i in range(4):
    app.grid_rowconfigure(i, weight=1)
app.grid_columnconfigure(1, weight=1)

entry_tickers.bind('<FocusIn>', clear_tickers_placeholder)
entry_period.bind('<FocusIn>', clear_period_placeholder)

df_close_prices = None

app.mainloop()