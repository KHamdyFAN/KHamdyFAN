import customtkinter as ctk
from tkinter import messagebox
from task_manager import authenticate_user, register_user


def login_ui(root, on_login_success):
    """Create the modern login screen using customtkinter."""
    # Root configuration
    root.configure(fg_color="white")  # Set outer background color

    # Center frame with transparent background
    frame = ctk.CTkFrame(root, corner_radius=15, fg_color="transparent")
    frame.pack(pady=50, padx=50)

    # Title Label
    title_label = ctk.CTkLabel(frame, text="Login", font=("Helvetica", 20, "bold"), text_color="black")
    title_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Username
    username_label = ctk.CTkLabel(frame, text="Username", font=("Helvetica", 14), text_color="black")
    username_label.grid(row=1, column=0, pady=10, sticky="w")
    username_entry = ctk.CTkEntry(frame, width=250, placeholder_text="Enter username")
    username_entry.grid(row=1, column=1, pady=10)

    # Password
    password_label = ctk.CTkLabel(frame, text="Password", font=("Helvetica", 14), text_color="black")
    password_label.grid(row=2, column=0, pady=10, sticky="w")
    password_entry = ctk.CTkEntry(frame, width=250, placeholder_text="Enter password", show="*")
    password_entry.grid(row=2, column=1, pady=10)

    # Button Handlers
    def handle_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Input Error", "Username and Password cannot be empty.")
            return
        if authenticate_user(username, password):
            on_login_success(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def handle_register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Input Error", "Username and Password cannot be empty.")
            return
        if register_user(username, password):
            messagebox.showinfo("Registration Successful", "You can now log in.")
        else:
            messagebox.showerror("Registration Failed", "Username already exists.")

    # Buttons
    login_button = ctk.CTkButton(frame, text="Login", command=handle_login, corner_radius=10)
    login_button.grid(row=3, column=0, pady=20, padx=10)

    register_button = ctk.CTkButton(frame, text="Register", command=handle_register, corner_radius=10)
    register_button.grid(row=3, column=1, pady=20, padx=10)

    # Exit Button
    exit_button = ctk.CTkButton(frame, text="Exit", fg_color="red", command=root.quit, corner_radius=10)
    exit_button.grid(row=4, column=0, columnspan=2, pady=10)
