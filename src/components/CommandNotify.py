import tkinter as tk
import threading
import time


class CommandNotify:
    def __init__(self, frame, send_callback):
        self.frame = frame
        self.send_callback = send_callback

        self.yolo_detect = {
            "label": "",
            "conf": "",
            "warn": "",
        }
        self.yolo_detect_old = dict(self.yolo_detect)

        self.box = tk.Frame(
            self.frame,
            highlightbackground="black",
            highlightthickness=1,
            width=640,
            height=240,
        )
        self.box.place(x=120, y=270)

        self.label = tk.Label(
            self.box, text="There are no forest fires", fg="green", font=("Arial", 12)
        )
        self.label.place(x=0, y=0, relwidth=1, relheight=0.2)

        self.flytime_label = tk.Label(self.box, text="Flytime: 0s", font=("Arial", 10))
        self.flytime_label.place(x=0, y=80, relwidth=1, relheight=0.2)

        self.arm_button = tk.Button(self.box, text="Arm", command=self.arm)
        self.arm_button.place(x=10, y=50, width=80, height=30)

        self.disarm_button = tk.Button(self.box, text="Disarm", command=self.disarm)
        self.disarm_button.place(x=100, y=50, width=80, height=30)

        self.takeoff_button = tk.Button(
            self.box, text="Takeoff(m)", command=self.takeoff
        )
        self.takeoff_button.place(x=190, y=50, width=80, height=30)

        self.altitude_entry = tk.Entry(self.box, justify="center")
        self.altitude_entry.place(x=280, y=50, width=80, height=30)
        self.altitude_entry.insert(0, "10")  # Default altitude

        self.mode_var = tk.StringVar(value="POS")
        self.mode_menu = tk.OptionMenu(
            self.box,
            self.mode_var,
            "GUIDED",
            "ALT",
            "POS",
            "AUTO",
            command=self.change_mode,
        )
        self.mode_menu.place(x=370, y=50, width=80, height=30)

        self.land_button = tk.Button(self.box, text="Land", command=self.toggle_land)
        self.land_button.place(x=460, y=50, width=80, height=30)
        self.is_landed = True

        self.yolo_detect_last_update = time.time()
        self.fly_time_start = None
        self.flag_flying = False

        self.check_fire_thread = threading.Thread(
            target=self.check_fire_loop, daemon=True
        )
        self.check_fire_thread.start()

        self.flytime_update_thread = threading.Thread(
            target=self.update_flytime_loop, daemon=True
        )
        self.flytime_update_thread.start()

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

            self.yolo_detect_last_update = time.time()

    def check_fire_loop(self):
        while True:
            current_time = time.time()
            if current_time - self.yolo_detect_last_update > 5:
                if self.yolo_detect == self.yolo_detect_old:
                    self.label.config(
                        text="There are no forest fires",
                        fg="green",
                    )
            self.yolo_detect_old = dict(self.yolo_detect)
            time.sleep(2)

    def update_flytime_loop(self):
        while True:
            if self.fly_time_start is not None:
                elapsed_time = int(time.time() - self.fly_time_start)
                self.flytime_label.config(text=f"Flytime: {elapsed_time}s")
            time.sleep(1)

    def send_command(self, command, data):
        payload = {
            "stream": "controlMsg",
            "direction": "drone",
            "header": command,
            "data": data,
        }
        self.send_callback(payload)

    def arm(self):
        self.send_command("arm", True)

    def disarm(self):
        self.send_command("arm", False)

    def takeoff(self):
        altitude = int(self.altitude_entry.get())
        self.send_command("takeoff", altitude)
        self.fly_time_start = time.time()

    def toggle_land(self):
        if self.is_landed:
            self.send_command("land", False)
            self.fly_time_start = time.time()
        else:
            self.send_command("land", True)
            self.fly_time_start = None
        self.is_landed = not self.is_landed

    def change_mode(self, value):
        if value == "GUIDED":
            value = "GUIDED"
        elif value == "ALT":
            value = "ALT_HOLD"
        elif value == "POS":
            value = "POS_HOLD"
        elif value == "AUTO":
            value = "AUTO"
        self.send_command("change_mode", value)
