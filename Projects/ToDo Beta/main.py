import customtkinter as ctk
from ui import create_ui
from task_manager import load_tasks, save_tasks
from login import login_ui


def main():
    def on_login_success(username):
        root.title(f"Modern To-Do App - {username}")
        tasks = load_tasks(username)

        # Destroy login screen and load main UI
        for widget in root.winfo_children():
            widget.destroy()

        # Pass the 'logout' function to create_ui (no need to pass login_ui)
        create_ui(root, tasks, lambda t: save_tasks(username, t), logout)

    def logout():
        for widget in root.winfo_children():
            widget.destroy()
        login_ui(root, on_login_success)

    # Initialize customtkinter
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.geometry("700x500")
    root.title("To-Do App")

    # Start with the login UI
    login_ui(root, on_login_success)
    root.mainloop()


if __name__ == "__main__":
    main()
