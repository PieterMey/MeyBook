import tkinter as tk
import yfinance as yf
from tkinter import filedialog
from datetime import datetime
import yaml
import os

from custom_entry import CustomEntry
from fetch_close_prices import fetch_close_prices as fcp
from utils import save_output, load_output



class StockClosePricesApp:
    def __init__(self, master):
        self.master = master
        master.title("Stock Close Prices")

        self.create_inputs_widgets()
        self.create_buttons_widgets()
        self.create_output_widgets()
        self.create_ticker_list_widget()
        self.configure_app_sizes()

        # Initialize the global variable for info message
        self.info_box=None

        # Initialize the global variable for storing close prices data
        self.close_prices = None
        self.entry_tickers = None
        self.entry_period = None

        # Load previous output
        load_output(self.output)
        self.load_window_settings()

        # Set up window close callback
        master.protocol("WM_DELETE_WINDOW", self.save_window_settings)

        # Bind the window "<Configure>" event
        self.master.bind("<Configure>", self.on_window_configure)

    def create_ticker_list_widget(self):
        self.ticker_list_label = tk.Label(self.master, text="", anchor="w")
        self.ticker_list_label.grid(row=3, column=2, sticky="nsew")

    def create_inputs_widgets(self):
        # Create and set up the Load Tickers from File button
        load_file_button = tk.Button(self.master, text="Load Tickers from File", command=self.load_tickers_from_file)
        load_file_button.grid(row=0, column=0)

    def create_buttons_widgets(self):
        # Create and set up the Fetch button
        fetch_button = tk.Button(self.master, text="Fetch Close Prices", command=self.fetch_close_prices_wrapper)
        fetch_button.grid(row=2, column=0)

        # Create and set up the Save button
        save_button = tk.Button(self.master, text="Save to CSV", command=self.save_to_csv)
        save_button.grid(row=2, column=1)

        # Create and set up the Remove Output button
        remove_button = tk.Button(self.master, text="Remove Output", command=lambda: self.output.delete(1.0, tk.END))
        remove_button.grid(row=2, column=2)

    def create_output_widgets(self):
        # Create and set up the output Text widget and its scrollbar
        output_frame = tk.Frame(self.master)
        output_frame.grid(row=3, rowspan=2, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.output = tk.Text(output_frame, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(output_frame, command=self.output.yview)
        self.output.config(yscrollcommand=scrollbar.set)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def configure_app_sizes(self):
        # Configure row and column weights for the app grid
        self.master.grid_rowconfigure(0, weight=0)
        self.master.grid_rowconfigure(1, weight=0)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_rowconfigure(3, weight=2)
        self.master.grid_rowconfigure(4, weight=3)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
    
    def create_info_box(self, info_message):
        if self.info_box is None:
            # Create a new Toplevel widget for the info box
            self.info_box = tk.Toplevel(self.master)
            self.info_box.overrideredirect(True)
            self.info_box.geometry("+{}+{}".format(self.master.winfo_x(), self.master.winfo_y() + self.master.winfo_height() - 50))

            # Create a frame for the info box
            info_frame = tk.Frame(self.info_box, bg="red", bd=1, relief=tk.SOLID)
            info_frame.pack(fill=tk.BOTH, expand=True)

            # Create a label to display the info message
            info_label = tk.Label(info_frame, text=info_message, fg="white", bg="red", font=("TkDefaultFont",12,"bold"))
            info_label.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

            # Create a button to close the info box
            close_button = tk.Button(info_frame, text="X", bg="black", fg="white", bd=0, command=self.remove_info_box, font=("TkDefaultFont",12,"bold"))
            close_button.pack(side=tk.LEFT, padx=5, pady=5)


    def move_info_box(self, event):
        x, y = event.x_root, event.y_root
        info_x, info_y = self.info_box.winfo_rootx(), self.info_box.winfo_rooty()
        info_width, info_height = self.info_box.winfo_width(), self.info_box.winfo_height()

        if info_x < x < info_x + info_width and info_y < y < info_y + info_height:
            return

        self.info_box.geometry(f"+{x}+{y}")

    def remove_info_box(self):
        self.info_box.destroy()
        self.info_box = None


    def fetch_close_prices_wrapper(self):
        """
        Wrapper function to fetch close prices and display them in the output Text widget.
        """
        if self.entry_tickers is not None or self.entry_period is not None:
            self.close_prices = fcp(self.entry_tickers, self.entry_period)

            # Add a newline character before inserting the new close prices into the output Text widget
            now = datetime.now().strftime("%Y-%m-%d") # get current time in format "YYYY-MM-DD HH:MM:SS"
            self.output.insert(tk.END, '\n' + '------------------ Session Date: ' + now + '------------------' + '\n' + self.close_prices.to_string(index=False))

            save_output(self.output)
        else:
            self.create_info_box("You haven't provided tickers or a period. Check your loading file.")

    def save_to_csv(self):
        """
        Save the DataFrame containing close prices to a CSV file.

        Args:
            close_prices (pandas.DataFrame): A DataFrame containing the close prices.
        """
        if self.close_prices is not None:
            file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if file_path:
                # Save the DataFrame to a CSV file
                self.close_prices.to_csv(file_path, date_format="%Y-%m-%d %H:%M:%S", index=False)
            else:
                self.create_info_box("file_path not valid!")
        else:
            self.create_info_box("You have not searched for any close_prices!")

    def load_tickers_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yml"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
            self.entry_tickers = data["tickers"]
            self.entry_period = data["period"][0]
            self.ticker_list_label.config(text="Tickers: "+''.join(["\n"+ ticker for ticker in self.entry_tickers]))

    def save_window_settings(self):
        """Save the current size and position of the app to a file."""
        window_settings = {
            "x": self.master.winfo_x(),
            "y": self.master.winfo_y(),
            "width": self.master.winfo_width(),
            "height": self.master.winfo_height(),
        }
        with open("window_settings.yml", "w") as f:
            yaml.dump(window_settings, f)

        # Close the app
        self.master.destroy()

    def load_window_settings(self):
        """Load the saved size and position of the app and apply them."""
        window_settings_file = "window_settings.yml"
        if os.path.exists(window_settings_file):
            with open(window_settings_file, "r") as f:
                window_settings = yaml.load(f, Loader=yaml.FullLoader)
            self.master.geometry("{}x{}+{}+{}".format(window_settings["width"], window_settings["height"], window_settings["x"], window_settings["y"]))
    
    def on_window_configure(self, event):
        """Handle window configuration events (e.g. resize, maximize)"""
        # Check if the window is maximized
        is_maximized = self.master.attributes('-fullscreen')
        if is_maximized:
            # If the window is maximized, set its minimum size to its current size
            self.master.minsize(event.width, event.height)
        else:
            # If the window is not maximized, reset its minimum size to (1, 1)
            self.master.minsize(1, 1)


