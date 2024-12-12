import math
import tkinter as tk


class Attitude:

    def __init__(self, frame, send_callback):
        self.frame = frame
        self.send_callback = send_callback

        self.payload_socket_attitude = {
            "attitude": {
                "pitch": "",
                "roll": "",
                "yaw": "",
            },
            "velocity": {
                "vx": "",
                "vy": "",
                "vz": "",
            },
            "heading": "",
        }

        # Create the box frame
        self.box = tk.Frame(
            self.frame,
            highlightbackground="black",
            highlightthickness=1,
        )
        self.box.place(x=210, y=10)

        # Configure grid for dynamic resizing
        for i in range(4):  # 4 rows for labels
            self.box.grid_rowconfigure(i, weight=1)
        # fix width
        self.box.grid_columnconfigure(0, weight=1, minsize=100)
        self.box.grid_columnconfigure(1, weight=1, minsize=100)
        self.box.grid_columnconfigure(2, weight=1, minsize=100)
        self.box.grid_columnconfigure(3, weight=1, minsize=100)

        # Attitude Labels
        self.pitch_label = tk.Label(self.box, text="Pitch:")
        self.pitch_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.pitch_value = tk.Label(
            self.box, text=self.payload_socket_attitude["attitude"]["pitch"]
        )
        self.pitch_value.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.roll_label = tk.Label(self.box, text="Roll:")
        self.roll_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.roll_value = tk.Label(
            self.box, text=self.payload_socket_attitude["attitude"]["roll"]
        )
        self.roll_value.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.yaw_label = tk.Label(self.box, text="Yaw:")
        self.yaw_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.yaw_value = tk.Label(
            self.box, text=self.payload_socket_attitude["attitude"]["yaw"]
        )
        self.yaw_value.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        # Velocity Labels
        self.vx_label = tk.Label(self.box, text="Vx:")
        self.vx_label.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.vx_value = tk.Label(
            self.box, text=self.payload_socket_attitude["velocity"]["vx"]
        )
        self.vx_value.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        self.vy_label = tk.Label(self.box, text="Vy:")
        self.vy_label.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.vy_value = tk.Label(
            self.box, text=self.payload_socket_attitude["velocity"]["vy"]
        )
        self.vy_value.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

        self.vz_label = tk.Label(self.box, text="Vz:")
        self.vz_label.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
        self.vz_value = tk.Label(
            self.box, text=self.payload_socket_attitude["velocity"]["vz"]
        )
        self.vz_value.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

        # Heading Label
        self.heading_label = tk.Label(self.box, text="Heading:")
        self.heading_label.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        self.heading_value = tk.Label(
            self.box, text=self.payload_socket_attitude["heading"]
        )
        self.heading_value.grid(row=3, column=2, padx=5, pady=5, sticky="nsew")

    def rad_to_deg(self, rad):
        return rad * 180 / math.pi

    def update_socket(self, message):
        if message["header"] == "droneStatusAttitude":
            self.payload_socket_attitude = message["data"]
            self.pitch_value.config(
                text=f"{float(self.payload_socket_attitude['attitude']['pitch']):.2f} deg"
            )
            self.roll_value.config(
                text=f'{float(self.payload_socket_attitude["attitude"]["roll"]):.2f} deg'
            )
            self.yaw_value.config(
                text=f'{float(self.payload_socket_attitude["attitude"]["yaw"]):.2f} deg'
            )
            self.vx_value.config(
                text=f'{float(self.payload_socket_attitude["velocity"]["vx"]):.2f} m/s'
            )
            self.vy_value.config(
                text=f'{float(self.payload_socket_attitude["velocity"]["vy"]):.2f} m/s'
            )
            self.vz_value.config(
                text=f'{float(self.payload_socket_attitude["velocity"]["vz"]):.2f} m/s'
            )
            self.heading_value.config(
                text=f'{float(self.payload_socket_attitude["heading"]):.2f} deg'
            )

    def __enter__(self):
        return self
