import tkinter as tk


class InfoDrone:
    def __init__(self, frame, send_callback):
        self.frame = frame
        self.send_callback = send_callback

        self.payload_socket_info = {
            "firmware": "Ardupilot",
            "type": "X4",
            "mode": "XX",
            "battery": {
                "voltage": 12.3,
                "current": 20.0,
                "level": 40.0,
            },
            "heartbeat": 0.5,
            "armed": False,
            "flagDisiableArmed": "False",
            "status": "OK",
        }

        self.screen_width = frame.winfo_screenwidth()
        self.screen_height = frame.winfo_screenheight()

        self.box = tk.Frame(
            self.frame,
            highlightbackground="black",
            highlightthickness=1,
        )
        self.box.place(x=120, y=10)

        # Configure grid weights for dynamic resizing
        for i in range(10):  # 10 rows in total
            self.box.grid_rowconfigure(i, weight=0, minsize=18)
        self.box.grid_columnconfigure(0, weight=1)
        self.box.grid_columnconfigure(1, weight=1)

        self.firmware_label = tk.Label(self.box, text="Firmware:")
        self.firmware_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.firmware_value = tk.Label(
            self.box, text=self.payload_socket_info["firmware"]
        )
        self.firmware_value.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.type_label = tk.Label(self.box, text="Type:")
        self.type_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.type_value = tk.Label(self.box, text=self.payload_socket_info["type"])
        self.type_value.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.mode_label = tk.Label(self.box, text="Mode:")
        self.mode_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.mode_value = tk.Label(self.box, text=self.payload_socket_info["mode"])
        self.mode_value.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.battery_voltage_label = tk.Label(self.box, text="Voltage:")
        self.battery_voltage_label.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.battery_voltage_value = tk.Label(
            self.box, text=f'{self.payload_socket_info["battery"]["voltage"]:.2f} V'
        )
        self.battery_voltage_value.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        self.battery_current_label = tk.Label(self.box, text="Current:")
        self.battery_current_label.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        self.battery_current_value = tk.Label(
            self.box, text=f'{self.payload_socket_info["battery"]["current"]:.2f} A'
        )
        self.battery_current_value.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

        self.battery_level_label = tk.Label(self.box, text="Level:")
        self.battery_level_label.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")
        self.battery_level_value = tk.Label(
            self.box, text=f'{self.payload_socket_info["battery"]["level"]:.2f} %'
        )
        self.battery_level_value.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

        self.heartbeat_label = tk.Label(self.box, text="Heartbeat:")
        self.heartbeat_label.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")
        self.heartbeat_value = tk.Label(
            self.box, text=f'{self.payload_socket_info["heartbeat"]:.2f}'
        )
        self.heartbeat_value.grid(row=6, column=1, padx=5, pady=5, sticky="nsew")

        self.armed_label = tk.Label(self.box, text="Armed:")
        self.armed_label.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")
        self.armed_value = tk.Label(self.box, text=self.payload_socket_info["armed"])
        self.armed_value.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")

        self.flagDisableArmed_label = tk.Label(self.box, text="Disable Armed:")
        self.flagDisableArmed_label.grid(row=8, column=0, padx=5, pady=5, sticky="nsew")
        self.flagDisableArmed_value = tk.Label(
            self.box, text=self.payload_socket_info["flagDisiableArmed"]
        )
        self.flagDisableArmed_value.grid(row=8, column=1, padx=5, pady=5, sticky="nsew")

        self.status_label = tk.Label(self.box, text="Status:")
        self.status_label.grid(row=9, column=0, padx=5, pady=5, sticky="nsew")
        self.status_value = tk.Label(self.box, text=self.payload_socket_info["status"])
        self.status_value.grid(row=9, column=1, padx=5, pady=5, sticky="nsew")

    def update_socket(self, message):
        if (
            message["header"] == "droneStatusInfo"
            or message["header"] == "droneStatusInfor"
        ):
            self.payload_socket_info = message["data"]

            self.firmware_value.config(text=self.payload_socket_info["firmware"][3:])
            self.type_value.config(text=self.payload_socket_info["type"])
            self.mode_value.config(text=self.payload_socket_info["mode"])

            self.battery_voltage_value.config(
                text=f'{float(self.payload_socket_info["battery"]["voltage"]):.2f} V'
            )
            if (
                self.payload_socket_info["battery"]["current"] != "None"
                and self.payload_socket_info["battery"]["current"] is not None
            ):
                self.battery_current_value.config(
                    text=f'{float(self.payload_socket_info["battery"]["current"]):.2f} A'
                )
            if (
                self.payload_socket_info["battery"]["level"] != "None"
                and self.payload_socket_info["battery"]["level"] is not None
            ):
                self.battery_level_value.config(
                    text=f'{float(self.payload_socket_info["battery"]["level"]):.2f} %'
                )
            self.heartbeat_value.config(
                text=f'{float(self.payload_socket_info["heartbeat"]):.2f}'
            )
            self.armed_value.config(text=self.payload_socket_info["armed"])
            self.flagDisableArmed_value.config(
                text=self.payload_socket_info["flagDisiableArmed"]
            )

            self.status_value.config(text=self.payload_socket_info["status"])

    def __enter__(self):
        return self
