import tkinter as tk


class CommandNotify:
    def __init__(self, frame, send_callback):
        self.frame = frame
        self.send_callback = send_callback

        self.yolo_detect = {
            "label": "",
            "conf": "",
            "warn": "",
        }

        self.box = tk.Frame(
            self.frame,
            highlightbackground="black",
            highlightthickness=1,
            width=640,
            height=240,
        )
        self.box.place(x=120, y=252)

        self.label = tk.Label(
            self.box, text="There are no forest fires", fg="green", font=("Arial", 12)
        )
        self.label.place(x=0, y=0, relwidth=1, relheight=0.2)

        self.arm_button = tk.Button(self.box, text="Arm", command=self.arm)
        self.arm_button.place(x=10, y=50, width=80, height=30)

        self.takeoff_button = tk.Button(
            self.box, text="Takeoff(m)", command=self.takeoff
        )
        self.takeoff_button.place(x=100, y=50, width=80, height=30)

        self.altitude_entry = tk.Entry(self.box, justify="center")
        self.altitude_entry.place(x=190, y=50, width=80, height=30)
        self.altitude_entry.insert(0, "10")  # Default altitude

        self.mode_var = tk.StringVar(value="POS_HOLD")
        self.mode_menu = tk.OptionMenu(
            self.box,
            self.mode_var,
            "GUIDED",
            "ALT_HOLD",
            "POS_HOLD",
            "AUTO",
            command=self.change_mode,
        )
        self.mode_menu.place(x=280, y=50, width=80, height=30)

        self.land_button = tk.Button(self.box, text="Land", command=self.land)
        self.land_button.place(x=370, y=50, width=80, height=30)

    def update_socket(self, socket):
        if socket["header"] == "fireDetection":
            data = socket["data"]
            self.yolo_detect["label"] = data["label"]
            self.yolo_detect["conf"] = data["conf"]
            self.yolo_detect["warn"] = (
                "There is a forest fire here"
                if self.yolo_detect["conf"] > 0.5
                else "There are no forest fires"
            )

            self.label.config(
                text=f"{self.yolo_detect['label']}: {self.yolo_detect['conf']:.2f} ({self.yolo_detect['warn']})",
                fg="red" if self.yolo_detect["conf"] > 0.5 else "green",
            )

    def arm(self):
        print("Arming the drone")
        # Implement the arm logic here

    def takeoff(self):
        altitude = float(self.altitude_entry.get())
        print(f"Taking off to {altitude} meters")
        # Implement the takeoff logic here with the given altitude

    def land(self):
        print("Landing the drone")
        # Implement the land logic here

    def change_mode(self, value):
        print("Current mode:", value)
