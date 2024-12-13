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
            highlightthickness=1 if frame is not None else 0,
            width=640,
            height=480,
        )

        self.header_label = tk.Label(
            self.box, text="Video Streaming", font=("Arial", 12)
        )
        self.header_label.place(x=0, y=10, relwidth=1, relheight=0.1)

        self.video_label = tk.Label(self.box)
        self.video_label.place(x=0, y=60, relwidth=1, relheight=0.8)

        self.box.place(x=120, y=self.screen_height - 560)

    def update_video(self, frame):
        # Convert the frame to a format suitable for Tkinter
        cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        scale_percent = 90  # percent of original size
        width = int(cv2_image.shape[1] * scale_percent / 100)
        height = int(cv2_image.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(cv2_image, dim, interpolation=cv2.INTER_AREA)
        img = Image.fromarray(resized)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the label with the new image
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
