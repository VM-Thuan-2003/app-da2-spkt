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
        }

        self.screen_width = frame.winfo_screenwidth()
        self.screen_height = frame.winfo_screenheight()

        self.box = tk.Frame(
            self.frame, highlightbackground="black", highlightthickness=1
        )
        self.box.place(x=10, y=10)

        self.firmware_label = tk.Label(self.box, text="Firmware:")
        self.firmware_label.grid(row=0, column=0, padx=5, pady=5)
        self.firmware_value = tk.Label(
            self.box, text=self.payload_socket_info["firmware"]
        )
        self.firmware_value.grid(row=0, column=1, padx=5, pady=5)

        self.type_label = tk.Label(self.box, text="Type:")
        self.type_label.grid(row=1, column=0, padx=5, pady=5)
        self.type_value = tk.Label(self.box, text=self.payload_socket_info["type"])
        self.type_value.grid(row=1, column=1, padx=5, pady=5)

        self.mode_label = tk.Label(self.box, text="Mode:")
        self.mode_label.grid(row=2, column=0, padx=5, pady=5)
        self.mode_value = tk.Label(self.box, text=self.payload_socket_info["mode"])
        self.mode_value.grid(row=2, column=1, padx=5, pady=5)

        self.battery_voltage_label = tk.Label(self.box, text="Voltage:")
        self.battery_voltage_label.grid(row=3, column=0, padx=5, pady=5)
        self.battery_voltage_value = tk.Label(
            self.box, text=f'{self.payload_socket_info["battery"]["voltage"]:.2f} V'
        )
        self.battery_voltage_value.grid(row=3, column=1, padx=5, pady=5)

        self.battery_current_label = tk.Label(self.box, text="Current:")
        self.battery_current_label.grid(row=4, column=0, padx=5, pady=5)
        self.battery_current_value = tk.Label(
            self.box, text=f'{self.payload_socket_info["battery"]["current"]:.2f} A'
        )
        self.battery_current_value.grid(row=4, column=1, padx=5, pady=5)

        self.battery_level_label = tk.Label(self.box, text="Level:")
        self.battery_level_label.grid(row=5, column=0, padx=5, pady=5)
        self.battery_level_value = tk.Label(
            self.box, text=f'{self.payload_socket_info["battery"]["level"]:.2f} %'
        )
        self.battery_level_value.grid(row=5, column=1, padx=5, pady=5)

        self.heartbeat_label = tk.Label(self.box, text="Heartbeat:")
        self.heartbeat_label.grid(row=6, column=0, padx=5, pady=5)
        self.heartbeat_value = tk.Label(
            self.box, text=f'{self.payload_socket_info["heartbeat"]:.2f}'
        )
        self.heartbeat_value.grid(row=6, column=1, padx=5, pady=5)

        self.armed_label = tk.Label(self.box, text="Armed:")
        self.armed_label.grid(row=7, column=0, padx=5, pady=5)
        self.armed_value = tk.Label(self.box, text=self.payload_socket_info["armed"])
        self.armed_value.grid(row=7, column=1, padx=5, pady=5)

        self.flagDisableArmed_label = tk.Label(self.box, text="Disable Armed:")
        self.flagDisableArmed_label.grid(row=8, column=0, padx=5, pady=5)
        self.flagDisableArmed_value = tk.Label(
            self.box, text=self.payload_socket_info["flagDisiableArmed"]
        )
        self.flagDisableArmed_value.grid(row=8, column=1, padx=5, pady=5)

    def update_socket(self, message):
        if message["header"] == "droneStatusInfo":
            self.payload_socket_info = message["data"]

            self.firmware_value.config(text=self.payload_socket_info["firmware"])
            self.type_value.config(text=self.payload_socket_info["type"])
            self.mode_value.config(text=self.payload_socket_info["mode"])
            self.battery_voltage_value.config(
                text=f'{float(self.payload_socket_info["battery"]["voltage"]):.2f} V'
            )
            self.battery_current_value.config(
                text=f'{float(self.payload_socket_info["battery"]["current"]):.2f} A'
            )
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

    def __enter__(self):
        return self
