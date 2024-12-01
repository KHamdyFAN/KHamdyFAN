import tkinter as tk
from tkinter import filedialog, messagebox
from data_import import load_csv, load_json
from visualizations import plot_performance

data = None  # Global variable to store the loaded data


def load_data_file(load_button):
    """
    Function to load data from a file and disable the load button.
    """
    global data
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("JSON files", "*.json")])
    if file_path:
        if file_path.endswith('.csv'):
            data = load_csv(file_path)
        elif file_path.endswith('.json'):
            data = load_json(file_path)
        else:
            messagebox.showerror("Error", "Invalid file type")
            return
        load_button.config(state=tk.DISABLED)  # Disable the load button after loading data
    else:
        data = None


def display_plot(root, y_axis):
    """
    Function to display the plot based on the selected Y-axis value.
    """
    if not y_axis:
        messagebox.showerror("Error", "Please select a value for the Y-Axis")
        return
    if data is not None:
        # Remove any existing plot
        for widget in root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()
        # Generate and display the new plot
        chart = plot_performance(data, 'name', y_axis)
        if chart is not None:
            chart_label = tk.Label(root, image=chart, bg="lightgray")
            chart_label.image = chart
            chart_label.pack(pady=10, expand=True, fill=tk.BOTH)
    else:
        messagebox.showerror("Error", "No data to plot")


def main():
    """
    Main function to set up the GUI.
    """
    root = tk.Tk()
    root.title("Dashboard")
    root.geometry("800x600")
    root.configure(bg="lightgray")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    button_frame = tk.Frame(root, bg="lightgray")
    button_frame.pack(pady=10)

    # Load Data button
    load_button = tk.Button(button_frame, text="Load Data", command=lambda: load_data_file(load_button))
    load_button.grid(row=0, column=0, padx=10, pady=5)

    # Y-Axis selection
    y_axis_label = tk.Label(button_frame, text="Y-Axis:", bg="lightgray")
    y_axis_label.grid(row=0, column=1, padx=10, pady=5)
    y_axis_var = tk.StringVar(root)
    y_axis_menu = tk.OptionMenu(button_frame, y_axis_var, "math_score", "science_score", "history_score")
    y_axis_menu.grid(row=0, column=2, padx=10, pady=5)

    # Display Plot button
    plot_button = tk.Button(button_frame, text="Display Plot", command=lambda: display_plot(root, y_axis_var.get()))
    plot_button.grid(row=0, column=3, padx=10, pady=5)

    root.mainloop()
