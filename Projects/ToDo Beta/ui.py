import customtkinter as ctk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from PIL import Image
from progress import show_stats
import os
from datetime import datetime

tasks = []


def create_ui(root, tasks_list, save_tasks_callback, logout_callback):
    global tasks
    tasks = tasks_list

    # Configure the root window background and size
    root.configure(fg_color="white")
    root.geometry("1200x800")  # Increased GUI size

    # Main frame
    frame = ctk.CTkFrame(root, corner_radius=15, fg_color="transparent")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Title Label
    title_label = ctk.CTkLabel(frame, text="Task Manager", font=("Helvetica", 20, "bold"), text_color="black")
    title_label.pack(pady=10)

    # Task input fields
    input_frame = ctk.CTkFrame(frame, fg_color="transparent")
    input_frame.pack(pady=10)

    # Task Entry
    task_entry = ctk.CTkEntry(input_frame, width=200, placeholder_text="Enter Task")
    task_entry.grid(row=0, column=0, padx=10)

    # Start Date Calendar
    start_date_label = ctk.CTkLabel(input_frame, text="Start Date")
    start_date_label.grid(row=0, column=1, padx=10)
    start_date_entry = DateEntry(input_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
    start_date_entry.grid(row=0, column=2, padx=10)

    # Priority Dropdown
    priority_label = ctk.CTkLabel(input_frame, text="Priority")
    priority_label.grid(row=0, column=3, padx=10)
    priority_combobox = ttk.Combobox(input_frame, values=["Low", "Medium", "High"], state="readonly", width=15)
    priority_combobox.grid(row=0, column=4, padx=10)
    priority_combobox.set("Medium")

    # Status Dropdown
    status_label = ctk.CTkLabel(input_frame, text="Status")
    status_label.grid(row=0, column=5, padx=10)
    status_combobox = ttk.Combobox(input_frame, values=["Pending", "In Progress", "Done"], state="readonly", width=15)
    status_combobox.grid(row=0, column=6, padx=10)
    status_combobox.set("Pending")

    # Add Task Button (with smaller icon)
    try:
        add_icon = ctk.CTkImage(light_image=Image.open("resources/icons/add.png"), size=(15, 15))  # Reduced size
    except FileNotFoundError:
        add_icon = None  # Fallback if icon is not found

    add_task_button = ctk.CTkButton(
        input_frame,
        text="",
        image=add_icon,
        command=lambda: add_task(),
        width=25,  # Smaller button width
        height=25,
        corner_radius=10,
        fg_color="transparent"
    )
    add_task_button.grid(row=0, column=7, padx=10)

    # Task Treeview for displaying tasks
    treeview_frame = ctk.CTkFrame(frame, fg_color="transparent")
    treeview_frame.pack(pady=10, expand=True, fill="both")

    columns = ("Task", "Start Date", "Priority", "Status", "Progress")
    task_treeview = ttk.Treeview(treeview_frame, columns=columns, show="headings", height=10)

    # Define headings
    for col in columns:
        task_treeview.heading(col, text=col)
        task_treeview.column(col, anchor="center", width=150)

    task_treeview.pack(fill="both", expand=True)

    # Function to load tasks into Treeview
    def load_tasks_to_treeview():
        task_treeview.delete(*task_treeview.get_children())  # Clear existing data
        for task in tasks:
            task_treeview.insert(
                "", "end",
                values=(
                    task.get("task", "N/A"),
                    task.get("start_date", "N/A"),
                    task.get("priority", "N/A"),
                    task.get("status", "Pending"),
                    task.get("progress", "0")
                )
            )

    # Add Task Functionality
    def add_task():
        task = task_entry.get()
        start_date = start_date_entry.get_date().strftime("%Y-%m-%d")
        priority = priority_combobox.get()
        status = status_combobox.get()

        if task and start_date and priority and status:
            tasks.append({
                "task": task,
                "start_date": start_date,
                "priority": priority,
                "status": status,
                "progress": 0  # Initial progress is 0
            })
            task_entry.delete(0, "end")
            priority_combobox.set("Medium")
            status_combobox.set("Pending")
            save_tasks_callback(tasks)
            load_tasks_to_treeview()
        else:
            messagebox.showwarning("Input Error", "All fields must be filled.")

    # Edit Task Functionality
    def edit_task():
        selected_item = task_treeview.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")
            return

        # Retrieve the selected task data
        selected_task = task_treeview.item(selected_item[0])["values"]
        task_name = selected_task[0]
        start_date = selected_task[1]
        priority = selected_task[2]
        status = selected_task[3]
        progress = selected_task[4]

        # Populating the fields with selected task details
        task_entry.delete(0, "end")
        task_entry.insert(0, task_name)

        # Convert start_date string to datetime.date object
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            start_date_entry.set_date(start_date_obj)
        except ValueError:
            messagebox.showwarning("Date Error", "The start date format is incorrect.")

        priority_combobox.set(priority)
        status_combobox.set(status)

        # Create the progress slider with title
        progress_label = ctk.CTkLabel(frame, text="Progress")
        progress_label.pack(pady=5)

        try:
            progress_value = int(float(progress))  # Convert to int after rounding
        except ValueError:
            progress_value = 0  # Default to 0 if conversion fails

        progress_slider = ctk.CTkSlider(frame, from_=0, to=100, number_of_steps=101, width=200, command=None)
        progress_slider.set(progress_value)  # Set the current progress as int
        progress_slider.pack(pady=10)

        # Create a label to show the progress percentage
        progress_percentage_label = ctk.CTkLabel(frame, text=f"{progress_value}%")
        progress_percentage_label.pack(pady=5)

        # Update the progress percentage dynamically
        def update_progress_label(value):
            progress_percentage_label.configure(text=f"{int(value)}%")

        # Bind the slider to update the label dynamically
        progress_slider.configure(command=update_progress_label)

        # Allow the user to update the task
        def update_task():
            tasks_index = next((index for (index, d) in enumerate(tasks) if d["task"] == task_name), None)
            if tasks_index is not None:
                tasks[tasks_index] = {
                    "task": task_entry.get(),
                    "start_date": start_date_entry.get_date().strftime("%Y-%m-%d"),
                    "priority": priority_combobox.get(),
                    "status": status_combobox.get(),
                    "progress": int(progress_slider.get())  # Update progress based on slider value as int
                }
                save_tasks_callback(tasks)
                load_tasks_to_treeview()

            # Hide the Progress slider, label, and Update button after update
            progress_label.pack_forget()
            progress_slider.pack_forget()
            progress_percentage_label.pack_forget()
            update_button.pack_forget()

        update_button = ctk.CTkButton(frame, text="Update Task", command=update_task)
        update_button.pack(pady=10)

    # Show Stats Button
    def show_stats_button():
        show_stats(tasks)

    show_stats_button = ctk.CTkButton(frame, text="Show Stats", command=show_stats_button, corner_radius=10)
    show_stats_button.pack(pady=10)

    # Edit Task Button (now placed under Show Stats)
    edit_task_button = ctk.CTkButton(
        frame,
        text="Edit Task",
        command=lambda: edit_task(),
        corner_radius=10
    )
    edit_task_button.pack(pady=10)

    # Logout Button
    logout_button = ctk.CTkButton(frame, text="Logout", command=logout_callback, fg_color="red", corner_radius=10)
    logout_button.pack(pady=10)

    # Load tasks to the treeview when the app starts
    load_tasks_to_treeview()