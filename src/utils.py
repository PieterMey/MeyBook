from datetime import datetime
import tkinter as tk

def save_output(output):
    """
    Save the output to a file with the current month and year.
    """
    current_month_year = datetime.now().strftime("%Y-%m")
    file_name = f"output_{current_month_year}.txt"
    with open(file_name, "w") as file:
        file.write(output.get(1.0, tk.END))

def load_output(output):
    """
    Load the output from a file with the current month and year if it exists.
    """
    current_month_year = datetime.now().strftime("%Y-%m")
    file_name = f"output_{current_month_year}.txt"
    try:
        with open(file_name, "r") as file:
            output.insert(tk.END, file.read())
    except FileNotFoundError:
        pass