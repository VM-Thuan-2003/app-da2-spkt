import tkinter as tk
from src.components.tkintermapview import TkinterMapView
import requests


class GetGpsRequest:
    def __init__(self):
        self.response = requests.get("https://ipinfo.io/json")
        self.data = self.response.json()

    def get_coordinates(self):
        return tuple(map(float, self.data["loc"].split(",")))

    def get_address(self):
        return f"Street: {self.data.get('street', 'N/A')}, City: {self.data.get('city', 'N/A')}, Region: {self.data.get('region', 'N/A')}, Country: {self.data.get('country', 'N/A')}"

    def get_info(self):
        coordinates = self.get_coordinates()
        address = self.get_address()
        return coordinates, address


class Map:
    def __init__(self, frame, send_callback):
        self.frame = frame
        self.send_callback = send_callback

        self.count = 0

        self.current_marker = None
        self.curr_position = None

        self.marker_path = None
        self.marker_list = []

        self.gps_init = GetGpsRequest()
        self.gps_lat_lon_init = self.gps_init.get_coordinates()

        # Box container
        self.box = tk.Frame(
            self.frame, highlightbackground="black", highlightthickness=1
        )
        self.box.place(relwidth=0.5, relheight=0.9, relx=0.48, rely=0.08)

        self.box.grid_columnconfigure(0, weight=1)
        self.box.grid_columnconfigure(1, weight=3)
        self.box.grid_rowconfigure(0, weight=1)

        # Left frame
        self.frame_left = tk.Frame(master=self.box, bg="lightgrey")
        self.frame_left.grid(row=0, column=0, sticky="nsew")
        self.frame_left.grid_rowconfigure(0, weight=0)
        self.frame_left.grid_rowconfigure(1, weight=0)
        self.frame_left.grid_rowconfigure(2, weight=1)
        self.frame_left.grid_columnconfigure(0, weight=1)

        self.button_1 = tk.Button(
            master=self.frame_left, text="Set Marker", command=self.set_marker_event
        )
        self.button_1.grid(pady=(10, 0), padx=(10, 10), row=0, column=0, sticky="ew")

        self.button_2 = tk.Button(
            master=self.frame_left, text="Clear Marker", command=self.clear_marker_event
        )
        self.button_2.grid(pady=(10, 0), padx=(10, 10), row=1, column=0, sticky="ew")

        self.map_option_menu = tk.OptionMenu(
            self.frame_left,
            tk.StringVar(value="OpenStreetMap"),
            "OpenStreetMap",
            "Google normal",
            "Google satellite",
            "Painting",
            "Black and White",
            "Hiking",
            "No labels",
            "Swisstopo",
            command=self.change_map,
        )
        self.map_option_menu.grid(
            row=3, column=0, padx=(10, 10), pady=(10, 0), sticky="ew"
        )

        self.altitude_label = tk.Label(
            self.frame_left, text="Altitude (m):", anchor="w"
        )
        self.altitude_label.grid(
            row=4, column=0, padx=(10, 10), pady=(10, 0), sticky="ew"
        )

        self.altitude_entry = tk.Entry(master=self.frame_left)
        self.altitude_entry.insert(0, "10")
        self.altitude_entry.grid(
            row=5, column=0, padx=(10, 10), pady=(10, 0), sticky="ew"
        )

        self.velocity_label = tk.Label(
            self.frame_left, text="Velocity (m/s):", anchor="w"
        )
        self.velocity_label.grid(
            row=6, column=0, padx=(10, 10), pady=(10, 0), sticky="ew"
        )

        self.velocity_entry = tk.Entry(master=self.frame_left)
        self.velocity_entry.insert(0, "2")
        self.velocity_entry.grid(
            row=7, column=0, padx=(10, 10), pady=(10, 0), sticky="ew"
        )

        self.button_3 = tk.Button(
            master=self.frame_left,
            text="Load Waypoints",
            command=self.load_waypoints_event,
        )
        self.button_3.grid(pady=(10, 0), padx=(10, 10), row=8, column=0, sticky="ew")

        # Right frame
        self.frame_right = tk.Frame(master=self.box, bg="white")
        self.frame_right.grid(row=0, column=1, sticky="nsew")
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_columnconfigure(0, weight=1)

        self.entry = tk.Entry(master=self.frame_right)
        self.entry.grid(row=0, column=0, sticky="ew", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = tk.Button(
            master=self.frame_right, text="Search", width=12, command=self.search_event
        )
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        self.map_widget = TkinterMapView(self.frame_right)
        self.map_widget.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.map_widget.set_tile_server(
            "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
        )
        self.map_widget.set_zoom(18)
        self.map_widget.set_position(
            self.gps_lat_lon_init[0], self.gps_lat_lon_init[1], marker=False
        )
        self.map_widget.add_right_click_menu_command(
            label="add point",
            command=self.add_marker_event,
            pass_coords=True,
        )

        self.marker_list_text = tk.Text(
            self.frame_right, height=10, width=20, font=("Helvetica", 10)
        )
        self.marker_list_text.grid(row=2, column=0, columnspan=2, sticky="ew")

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def set_marker_event(self, event=None):
        current_position = self.map_widget.get_position()
        altitude = self.altitude_entry.get()
        velocity = self.velocity_entry.get()
        try:
            altitude = int(altitude)
        except ValueError:
            altitude = 10

        try:
            velocity = float(velocity)
        except ValueError:
            velocity = 2

        marker = self.map_widget.set_marker(
            current_position[0],
            current_position[1],
            text=f"point {len(self.marker_list) + 1}",
            marker_color_outside="blue",
        )
        self.marker_list.append(
            {
                "marker": marker,
                "position": current_position,
                "altitude": altitude,
                "velocity": velocity,
            }
        )
        self.update_marker_list_text()

    def add_marker_event(self, coords):
        new_marker = self.map_widget.set_marker(
            coords[0],
            coords[1],
            text=f"point {len(self.marker_list) + 1}",
            marker_color_outside="blue",
        )
        altitude = self.altitude_entry.get()
        velocity = self.velocity_entry.get()
        self.marker_list.append(
            {
                "marker": new_marker,
                "position": coords,
                "altitude": altitude,
                "velocity": velocity,
            }
        )
        self.update_marker_list_text()

    def connect_marker(self):
        if len(self.marker_list) > 1:
            position_list = [marker["position"] for marker in self.marker_list]
            print(position_list)

            if self.marker_path:
                self.map_widget.delete(self.marker_path)
            if position_list:
                self.marker_path = self.map_widget.set_path(position_list)

    def clear_marker_event(self):
        for marker_dict in self.marker_list:
            marker_dict["marker"].delete()
        self.marker_list.clear()
        if self.marker_path:
            self.map_widget.delete(self.marker_path)
            self.marker_path = None
        self.update_marker_list_text()

    def change_map(self, new_map_type):
        if new_map_type == "OpenStreetMap":
            self.map_widget.set_tile_server(
                "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=19
            )
        elif new_map_type == "Google normal":
            self.map_widget.set_tile_server(
                "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
                max_zoom=22,
            )
        elif new_map_type == "Google satellite":
            self.map_widget.set_tile_server(
                "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
                max_zoom=22,
            )
        elif new_map_type == "Painting":
            self.map_widget.set_tile_server(
                "http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png"
            )
        elif new_map_type == "Black and White":
            self.map_widget.set_tile_server(
                "http://a.tile.stamen.com/toner/{z}/{x}/{y}.png"
            )
        elif new_map_type == "Hiking":
            self.map_widget.set_tile_server(
                "https://tiles.wmflabs.org/hikebike/{z}/{x}/{y}.png"
            )
        elif new_map_type == "No labels":
            self.map_widget.set_tile_server(
                "https://tiles.wmflabs.org/osm-no-labels/{z}/{x}/{y}.png"
            )
        elif new_map_type == "Swisstopo":
            self.map_widget.set_tile_server(
                "https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg"
            )

    def send_command(self, command, data):
        payload = {
            "stream": "controlMsg",
            "direction": "drone",
            "header": command,
            "data": data,
        }
        self.send_callback(payload)

    def load_waypoints_event(self):
        serializable_marker_list = [
            {
                "position": marker["position"],
                "altitude": marker.get("altitude"),
                "velocity": marker.get("velocity"),
                "text": marker["marker"].text,
            }
            for marker in self.marker_list
        ]
        self.send_command("loadWaypoints", serializable_marker_list)

    def update_marker_list_text(self):
        text = ""
        for i, marker_dict in enumerate(self.marker_list):
            text += f"Marker {i+1}: Lat: {marker_dict['position'][0]:.6f}, Lon: {marker_dict['position'][1]:.6f}, Altitude: {marker_dict['altitude']} m, Velocity: {marker_dict['velocity']} m/s\n"
        self.marker_list_text.delete(1.0, tk.END)
        self.marker_list_text.insert(tk.END, text)
        self.connect_marker()

    def update_current_position(self):

        if self.current_marker:
            self.map_widget.delete(self.current_marker)

        self.current_marker = self.map_widget.set_marker(
            float(self.curr_position[0]),
            float(self.curr_position[1]),
            text="Current Position",
            marker_color_outside="red",
        )

        self.count += 1
        if self.count >= 10:
            self.count = 0
            self.map_widget.set_position(
                float(self.curr_position[0]), float(self.curr_position[1]), marker=False
            )

    def update_socket(self, message):
        if message["header"] == "droneStatusGps":
            # print(f"updating map {message}")
            self.curr_position = message["data"]["lat"], message["data"]["lon"]
            self.update_current_position()
