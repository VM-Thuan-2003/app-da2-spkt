import tkinter as tk
from tkinter import messagebox
from src.firebase_manager import FirebaseManager
from src.socket_manager import SocketManager
from src.gui_manager import MainWindow, LoginWindow, RegisterWindow
from src.author import Role, Authorization
from config import SERVER


class MyApp:
    """Main application that integrates SocketManager and Firebase Authentication."""

    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.socket_manager = SocketManager(self.update_gui_label)
        self.authorization = Authorization(Role.GUEST)
        self.main_window = None
        # Start with the login screen
        self.show_login_window()

    def show_login_window(self):
        """Display the login window."""
        self.login_window = LoginWindow(
            self.root, self.login, self.show_register_window
        )

    def show_register_window(self):
        """Display the registration window."""
        self.login_window.destroy()
        self.register_window = RegisterWindow(
            self.root, self.register, self.show_login_window
        )

    def login(self, email, password):
        """Handle login logic with Firebase."""
        if email is None and password is None:
            self.socket_manager.start(SERVER)
            self.login_window.destroy()
            self.show_main_window({"name": "Guest", "role": Role.GUEST})
        else:
            is_authenticated = FirebaseManager.login_user(email, password)
            if is_authenticated:
                name = email.split("@")[0]
                if name == "admin":
                    self.authorization = Authorization(Role.ADMIN)
                else:
                    self.authorization = Authorization(Role.USER)

                self.socket_manager.start(SERVER)
                self.login_window.destroy()

                self.show_main_window({"name": name, "role": self.authorization.role})
            else:
                messagebox.showerror("Login Error", "Invalid email or password.")

    def register(self, email, password):
        """Handle registration logic with Firebase."""
        success = FirebaseManager.register_user(email, password)
        if success:
            messagebox.showinfo("Registration Success", "User successfully registered.")
            self.register_window.destroy()
            self.show_login_window()
        else:
            messagebox.showerror("Registration Error", "Error during registration.")

    def logout_from_main(self):
        """Logout from the main application."""
        self.socket_manager.disconnect()
        if self.main_window:
            self.main_window.destroy()
        self.authorization = Authorization(Role.GUEST)
        self.show_login_window()

    def show_main_window(self, payload):
        """Show the main application window."""
        self.main_window = MainWindow(
            self.root, self.send_message, self.logout_from_main, payload
        )

    def send_message(self, message):
        """Send a message to the Socket.IO server."""
        self.socket_manager.send_message(message)

    def update_gui_label(self, text):
        """Update the label via the GUI manager."""
        if self.main_window:
            self.main_window.update_socket(text)


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
