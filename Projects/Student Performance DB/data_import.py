import pandas as pd
from tkinter import messagebox


def load_csv(file_path):
    """
    Function to load data from a CSV file.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")
        return None


def load_json(file_path):
    """
    Function to load data from a JSON file.
    """
    try:
        data = pd.read_json(file_path)
        return data
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")
        return None
