import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from src.author import Role

from src.components import InfoDrone, Attitude, Gps


class Drone:
    def __init__(self, frame):
        pass

    def __enter__(self):
        return self


class Logo:
    def __init__(self, frame, src, width=100, height=100, x=0, y=0):
        self.frame = frame
        self.src = Path(src)
        self.logo = tk.PhotoImage(file=self.src)
        self.logo_label = tk.Label(self.frame, image=self.logo)
        self.logo_label.image = self.logo  # keep a reference
        self.logo_label.place(
            relx=x, rely=y, relwidth=width, relheight=height, anchor="center"
        )

    def __enter__(self):
        return self


class InfoTeam:
    """This class represents the information of a team."""

    def __init__(self, frame):
        self.screen_width = frame.winfo_screenwidth()
        self.screen_height = frame.winfo_screenheight()

        self.frame = tk.Frame(frame, highlightbackground="black", highlightthickness=0)
        self.frame.place(relx=0.5, rely=0.9, anchor="center")

        self.name = tk.Label(self.frame, text="Thanh vien nhom", font=("Roboto", 14))
        self.name.grid(row=0, column=0, columnspan=2)

        self.name_label_1 = tk.Label(
            self.frame, text="Le Thi Tuyet Nhi", font=("Roboto", 12)
        )
        self.name_label_1.grid(row=1, column=0)

        self.mssv_label_1 = tk.Label(
            self.frame, text="MSSV: 21161344", font=("Roboto", 12)
        )
        self.mssv_label_1.grid(row=1, column=1)

        self.name_label_2 = tk.Label(
            self.frame, text="Vo Minh Thuan", font=("Roboto", 12)
        )
        self.name_label_2.grid(row=2, column=0)

        self.mssv_label_2 = tk.Label(
            self.frame, text="MSSV: 21161366", font=("Roboto", 12)
        )
        self.mssv_label_2.grid(row=2, column=1)

        self.gvhd = tk.Label(
            self.frame, text="Giao vien huong dan", font=("Roboto", 14)
        )

        self.gvhd.grid(row=3, column=0, columnspan=2)

        self.name_gvhd = tk.Label(
            self.frame, text="Th.s Nguyen Ngo Lam", font=("Roboto", 12)
        )
        self.name_gvhd.grid(row=4, column=0, columnspan=2)

    def __enter__(self):
        return self


class GUIManager:
    """This class manages the static, default elements of the GUI and window properties."""

    def __init__(self, root):
        """Initialize the static GUI components and window properties."""
        self.root = root

        # Set window title and geometry
        self.root.title("Decentralized Tkinter with Socket.IO")
        self.screen_width = int(self.root.winfo_screenwidth() * 0.8)
        self.screen_height = int(self.root.winfo_screenheight() * 0.8)
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")


class MainWindow(GUIManager):
    """This class creates the main window of the application."""

    def __init__(
        self,
        root,
        send_callback,
        logout_callback,
        user={"name": "GUEST", "role": Role.GUEST},
    ):
        """Initialize the main window."""
        super().__init__(root)  # Initialize default GUI elements
        self.send_callback = send_callback
        self.logout_callback = logout_callback
        self.user = user

        self.frame = tk.Frame(root, width=self.screen_width, height=self.screen_height)
        self.frame.pack()

        # Label to display user name and role
        self.name_role = tk.Label(
            root,
            text=f"{self.user['name']} ({self.user['role'].name})",
            font=("Arial", 12),
        )
        self.name_role.place(relx=0.99, rely=0.01, anchor="ne")

        # Button to logout
        self.logout_button = tk.Button(root, text="Logout", command=self.logout)
        self.logout_button.place(relx=0.99, rely=0.04, anchor="ne")

        # Info Drone
        self.infoDrone = InfoDrone.InfoDrone(root, send_callback=self.send_callback)

        self.attitude = Attitude.Attitude(root, send_callback=self.send_callback)

        self.gps = Gps.Gps(root, send_callback=self.send_callback)

    def update_socket(self, message):
        """Update the label with a new message from the server."""
        self.infoDrone.update_socket(message)
        self.attitude.update_socket(message)
        self.gps.update_socket(message)

    def logout(self):
        """Logout and go back to the login window."""
        self.logout_callback()
        self.destroy()

    def destroy(self):
        """Destroy the main window frame."""
        self.frame.destroy()


class LoginWindow(GUIManager):
    """Class for handling the login window."""

    def __init__(self, root, on_login_callback, on_register_callback):
        """Initialize the login window."""
        super().__init__(root)  # Initialize default GUI elements
        self.on_login_callback = on_login_callback
        self.on_register_callback = on_register_callback

        self.frame = tk.Frame(root)
        self.frame.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1
        )  # Center the frame and set width and height to 50% of the screen

        # Logo
        Logo(self.frame, "logo.png", x=0.5, y=0.1, width=1, height=0.2)

        # Drone
        Logo(self.frame, "img_drone.png", x=0.1, y=0.5, width=0.4, height=0.5)

        # Information of the team
        InfoTeam(self.frame)

        box = tk.Frame(self.frame, highlightbackground="black", highlightthickness=1)
        box.place(relx=0.5, rely=0.5, anchor="center")
        # Email
        self.email_label = tk.Label(box, text="Email:")
        self.email_label.grid(row=0, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(box, width=30)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password
        self.password_label = tk.Label(box, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(box, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Container for the login and register buttons
        button_frame = tk.Frame(box)
        button_frame.grid(row=2, columnspan=2, pady=10)

        # Login button
        self.login_button = tk.Button(button_frame, text="Login", command=self.login)
        self.login_button.pack(side=tk.LEFT, padx=5)

        # Login no Account button
        self.login_no_account_button = tk.Button(
            button_frame, text="Login no Account", command=self.login_no_account
        )
        self.login_no_account_button.pack(side=tk.LEFT, padx=5)

        # Register button
        self.register_button = tk.Button(
            button_frame, text="Register", command=self.register
        )
        self.register_button.pack(side=tk.LEFT, padx=5)

    def login(self):
        """Handle the login button click."""
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email and password:
            self.on_login_callback(email, password)
        else:
            messagebox.showwarning(
                "Input Error", "Please enter both email and password."
            )

    def login_no_account(self):
        """Handle the login button click."""
        self.on_login_callback(None, None)

    def register(self):
        """Switch to the register form."""
        self.on_register_callback()

    def destroy(self):
        """Destroy the login window frame."""
        self.frame.destroy()


class RegisterWindow(GUIManager):
    """Class for handling the registration window."""

    def __init__(self, root, on_register_callback, on_back_to_login_callback):
        """Initialize the registration window."""
        super().__init__(root)  # Initialize default GUI elements
        self.on_register_callback = on_register_callback
        self.on_back_to_login_callback = on_back_to_login_callback

        self.frame = tk.Frame(root)
        self.frame.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1
        )  # Center the frame and set width and height to 50% of the screen

        # Logo
        Logo(self.frame, "logo.png", x=0.5, y=0.1, width=1, height=0.2)

        # Drone
        Logo(self.frame, "img_drone.png", x=0.1, y=0.5, width=0.4, height=0.5)
        # Information of the team
        InfoTeam(self.frame)

        box = tk.Frame(self.frame, highlightbackground="black", highlightthickness=1)
        box.place(relx=0.5, rely=0.5, anchor="center")

        # Email
        self.email_label = tk.Label(box, text="Email:")
        self.email_label.grid(row=0, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(box, width=30)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password
        self.password_label = tk.Label(box, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(box, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Confirm password
        self.confirm_password_label = tk.Label(box, text="Confirm Password:")
        self.confirm_password_label.grid(row=2, column=0, padx=5, pady=5)
        self.confirm_password_entry = tk.Entry(box, width=30, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)

        # Register button
        self.frame_button = tk.Frame(box)
        self.frame_button.grid(row=3, columnspan=2, pady=10)

        self.register_button = tk.Button(
            self.frame_button, text="Register", command=self.register
        )
        self.register_button.pack(side=tk.LEFT, padx=5)

        self.back_button = tk.Button(
            self.frame_button, text="Back to Login", command=self.back_to_login
        )
        self.back_button.pack(side=tk.LEFT, padx=5)

    def register(self):
        """Handle the register button click."""
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if email and password and confirm_password:
            if password == confirm_password:
                self.on_register_callback(email, password)
            else:
                messagebox.showwarning("Input Error", "Passwords do not match.")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def back_to_login(self):
        """Switch back to the login window."""
        self.destroy()
        self.on_back_to_login_callback()

    def destroy(self):
        """Destroy the registration window frame."""
        self.frame.destroy()
