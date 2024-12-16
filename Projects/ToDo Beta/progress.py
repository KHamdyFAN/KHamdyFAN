import customtkinter as ctk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime


def show_stats(tasks):
    # Create a new window for stats
    stats_window = ctk.CTkToplevel()
    stats_window.title("Task Progress Stats")
    stats_window.geometry("800x600")

    # Title Label
    title_label = ctk.CTkLabel(stats_window, text="Task Progress Stats", font=("Helvetica", 20, "bold"),
                               text_color="black")
    title_label.pack(pady=20)

    # Treeview to show task details
    columns = ("Task", "Status", "Progress")
    task_treeview = ttk.Treeview(stats_window, columns=columns, show="headings", height=10)

    for col in columns:
        task_treeview.heading(col, text=col)
        task_treeview.column(col, anchor="center", width=200)

    task_treeview.pack(fill="both", expand=True, pady=20)

    # Insert tasks into treeview
    for task in tasks:
        task_treeview.insert(
            "", "end",
            values=(
                task.get("task", "N/A"),
                task.get("status", "Pending"),
                task.get("progress", "0")
            )
        )

    # Track the current canvas
    current_canvas = None

    # Remove the current canvas if there is one
    def remove_current_canvas():
        nonlocal current_canvas
        if current_canvas:
            current_canvas.get_tk_widget().destroy()
            current_canvas = None

    # Pie chart for task status (inside the GUI)
    def plot_task_status():
        remove_current_canvas()

        status_count = {"Pending": 0, "In Progress": 0, "Done": 0}

        for task in tasks:
            status = task.get("status", "Pending")
            if status in status_count:
                status_count[status] += 1

        labels = status_count.keys()
        sizes = status_count.values()

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures pie chart is circular.

        # Create a new canvas and embed it in the window
        nonlocal current_canvas
        current_canvas = FigureCanvasTkAgg(fig, master=stats_window)
        current_canvas.get_tk_widget().pack(pady=10)
        current_canvas.draw()

    # Bar chart for task progress
    def plot_task_progress():
        remove_current_canvas()

        task_names = [task.get("task", "N/A") for task in tasks]
        task_progress = [task.get("progress", 0) for task in tasks]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(task_names, task_progress, color='skyblue')
        ax.set_xlabel('Progress (%)')
        ax.set_ylabel('Tasks')
        ax.set_title('Task Progress')

        nonlocal current_canvas
        current_canvas = FigureCanvasTkAgg(fig, master=stats_window)
        current_canvas.get_tk_widget().pack(pady=10)
        current_canvas.draw()

    # Bar chart for task count by priority
    def plot_task_priority():
        remove_current_canvas()

        priority_count = {"Low": 0, "Medium": 0, "High": 0}

        for task in tasks:
            priority = task.get("priority", "Medium")
            if priority in priority_count:
                priority_count[priority] += 1

        labels = priority_count.keys()
        sizes = priority_count.values()

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(labels, sizes, color='lightgreen')
        ax.set_xlabel('Priority')
        ax.set_ylabel('Task Count')
        ax.set_title('Task Count by Priority')

        nonlocal current_canvas
        current_canvas = FigureCanvasTkAgg(fig, master=stats_window)
        current_canvas.get_tk_widget().pack(pady=10)
        current_canvas.draw()

    # Line chart for task progress over time
    def plot_progress_over_time():
        remove_current_canvas()

        task_dates = [task.get("start_date", "N/A") for task in tasks]
        task_progress = [task.get("progress", 0) for task in tasks]

        # Convert start dates to datetime objects for plotting
        try:
            dates = [datetime.strptime(date, "%Y-%m-%d") for date in task_dates if date != "N/A"]
            progress = [task_progress[i] for i in range(len(task_progress)) if task_dates[i] != "N/A"]

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(dates, progress, marker='o', color='purple', linestyle='-', markersize=5)
            ax.set_xlabel('Date')
            ax.set_ylabel('Progress (%)')
            ax.set_title('Task Progress Over Time')
            plt.xticks(rotation=45)
            ax.grid(True)

            nonlocal current_canvas
            current_canvas = FigureCanvasTkAgg(fig, master=stats_window)
            current_canvas.get_tk_widget().pack(pady=10)
            current_canvas.draw()
        except ValueError:
            messagebox.showwarning("Date Error", "Some tasks do not have valid start dates.")

    # Histogram for task progress distribution
    def plot_progress_histogram():
        remove_current_canvas()

        task_progress = [task.get("progress", 0) for task in tasks]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(task_progress, bins=10, color='lightcoral', edgecolor='black')
        ax.set_xlabel('Progress (%)')
        ax.set_ylabel('Frequency')
        ax.set_title('Task Progress Distribution')

        nonlocal current_canvas
        current_canvas = FigureCanvasTkAgg(fig, master=stats_window)
        current_canvas.get_tk_widget().pack(pady=10)
        current_canvas.draw()

    # Add buttons for each graph
    plot_task_status_button = ctk.CTkButton(stats_window, text="Show Task Status Pie Chart", command=plot_task_status)
    plot_task_status_button.pack(pady=10)

    plot_task_progress_button = ctk.CTkButton(stats_window, text="Show Task Progress Bar Chart",
                                              command=plot_task_progress)
    plot_task_progress_button.pack(pady=10)

    plot_task_priority_button = ctk.CTkButton(stats_window, text="Show Task Count by Priority",
                                              command=plot_task_priority)
    plot_task_priority_button.pack(pady=10)

    plot_progress_over_time_button = ctk.CTkButton(stats_window, text="Show Progress Over Time",
                                                   command=plot_progress_over_time)
    plot_progress_over_time_button.pack(pady=10)

    plot_progress_histogram_button = ctk.CTkButton(stats_window, text="Show Progress Distribution Histogram",
                                                   command=plot_progress_histogram)
    plot_progress_histogram_button.pack(pady=10)

    stats_window.mainloop()
