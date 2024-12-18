import tkinter as tk


class Gps:
    def __init__(self, frame, send_callback):
        self.frame = frame
        self.send_callback = send_callback

        self.payload_socket_gps = {
            "sat": "",
            "fix": "",
            "Groundspeed": "",
            "lat": "",
            "lon": "",
            "alt": "",
            "homeLocation": {
                "lat": "",
                "lon": "",
                "alt": "",
            },
        }

        # Create the box frame
        self.box = tk.Frame(
            self.frame,
            highlightbackground="black",
            highlightthickness=1,
            width=300,
            height=300,
        )
        self.box.place(x=356, y=134)

        # Configure grid for fixed height and dynamic width
        for i in range(5):  # 5 rows for labels
            self.box.grid_rowconfigure(i, weight=1)
        for j in range(4):  # 4 columns for labels and values
            self.box.grid_columnconfigure(j, weight=1, minsize=92)

        # Gps Labels
        self.sat_label = tk.Label(self.box, text="Sat:")
        self.sat_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.sat_value = tk.Label(self.box, text=self.payload_socket_gps["sat"])
        self.sat_value.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        self.fix_label = tk.Label(self.box, text="Fix:")
        self.fix_label.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.fix_value = tk.Label(self.box, text=self.payload_socket_gps["fix"])
        self.fix_value.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

        self.groundspeed_label = tk.Label(self.box, text="Groundspeed:")
        self.groundspeed_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.groundspeed_value = tk.Label(
            self.box, text=self.payload_socket_gps["Groundspeed"]
        )
        self.groundspeed_value.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.airspeed_label = tk.Label(self.box, text="Airspeed:")
        self.airspeed_label.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.airspeed_value = tk.Label(
            self.box, text=self.payload_socket_gps["Groundspeed"]
        )
        self.airspeed_value.grid(row=1, column=3, padx=5, pady=5, sticky="nsew")

        self.latitude_label = tk.Label(self.box, text="Latitude:")
        self.latitude_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.latitude_value = tk.Label(self.box, text=self.payload_socket_gps["lat"])
        self.latitude_value.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.longitude_label = tk.Label(self.box, text="Longitude:")
        self.longitude_label.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
        self.longitude_value = tk.Label(self.box, text=self.payload_socket_gps["lon"])
        self.longitude_value.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        self.altitude_label = tk.Label(self.box, text="Altitude:")
        self.altitude_label.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
        self.altitude_value = tk.Label(self.box, text=self.payload_socket_gps["alt"])
        self.altitude_value.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

        self.home_lat_label = tk.Label(self.box, text="Home Latitude:")
        self.home_lat_label.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")
        self.home_lat_value = tk.Label(
            self.box, text=self.payload_socket_gps["homeLocation"]["lat"]
        )
        self.home_lat_value.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")

        self.home_lon_label = tk.Label(self.box, text="Home Longitude:")
        self.home_lon_label.grid(row=3, column=2, padx=5, pady=5, sticky="nsew")
        self.home_lon_value = tk.Label(
            self.box, text=self.payload_socket_gps["homeLocation"]["lon"]
        )
        self.home_lon_value.grid(row=3, column=3, padx=5, pady=5, sticky="nsew")

        self.home_alt_label = tk.Label(self.box, text="Home Altitude:")
        self.home_alt_label.grid(row=4, column=2, padx=5, pady=5, sticky="nsew")
        self.home_alt_value = tk.Label(
            self.box, text=self.payload_socket_gps["homeLocation"]["alt"]
        )
        self.home_alt_value.grid(row=4, column=3, padx=5, pady=5, sticky="nsew")

    def update_socket(self, message):
        if message["header"] == "droneStatusGps":
            self.payload_socket_gps = message["data"]

            self.sat_value.config(text=self.payload_socket_gps["sat"])
            self.fix_value.config(text=self.payload_socket_gps["fix"])
            self.groundspeed_value.config(
                text=f'{float(self.payload_socket_gps["Groundspeed"]):.2f} m/s'
            )
            self.airspeed_value.config(
                text=f'{float(self.payload_socket_gps["Groundspeed"]):.2f} m/s'
            )
            self.latitude_value.config(
                text=f'{float(self.payload_socket_gps["lat"]):.6f}'
            )
            self.longitude_value.config(
                text=f'{float(self.payload_socket_gps["lon"]):.6f}'
            )
            self.altitude_value.config(
                text=f'{float(self.payload_socket_gps["alt"]):.2f} m'
            )
            self.home_lat_value.config(
                text=f'{float(self.payload_socket_gps["homeLocation"]["lat"]):.6f}'
            )
            self.home_lon_value.config(
                text=f'{float(self.payload_socket_gps["homeLocation"]["lon"]):.6f}'
            )
            self.home_alt_value.config(
                text=f'{float(self.payload_socket_gps["homeLocation"]["alt"]):.2f} m'
            )

    def __enter__(self):
        return self
