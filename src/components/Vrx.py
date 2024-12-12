import tkinter as tk
from PIL import Image, ImageTk
import cv2


class Vrx:
    def __init__(self, frame, send_callback):
        self.frame = frame
        self.send_callback = send_callback

        self.screen_width = frame.winfo_screenwidth()
        self.screen_height = frame.winfo_screenheight()

        self.box = tk.Frame(
            self.frame,
            highlightbackground="black",
            highlightthickness=1,
        )

        self.video_label = tk.Label(self.box, width=640, height=480)
        self.video_label.pack()

        self.box.place(x=10, y=self.screen_height - 570)

    def update_video(self, frame):
        # Convert the frame to a format suitable for Tkinter
        cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2_image)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the label with the new image
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
