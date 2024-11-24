# app.py
import tkinter as tk
from tkinter import messagebox


def show_message():
    messagebox.showinfo("Hello", "Hello from your EXE!")


# Create the main window
root = tk.Tk()
root.title("Example App")
root.geometry("300x200")

# Create a button
button = tk.Button(root, text="Click Me", command=show_message)
button.pack(pady=20)

# Run the application
root.mainloop()
