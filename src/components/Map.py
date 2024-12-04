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
        super().__init__()
        self.frame = frame
        self.send_callback = send_callback

        self.screen_width = frame.winfo_screenwidth()
        self.screen_height = frame.winfo_screenheight()

        self.marker_list = []
        self.gps_init = GetGpsRequest()
        self.gps_lat_lon_init = self.gps_init.get_coordinates()

        self.box = tk.Frame(
            self.frame,
            width=300,
            height=300,
            highlightbackground="black",
            highlightthickness=1,
        )
        self.box.place(x=0, y=int(self.screen_height * 0.4))

        self.box.grid_columnconfigure(0, weight=0)
        self.box.grid_columnconfigure(1, weight=1)
        self.box.grid_rowconfigure(0, weight=1)
        self.box.place(x=int(self.screen_width - 720), y=int(self.screen_height - 430))
        self.frame_left = tk.Frame(master=self.box, width=10, height=40)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = tk.Frame(master=self.box, width=30, height=40)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        self.frame_right_right = tk.Frame(master=self.frame)
        self.frame_right_right.place(
            x=int(self.screen_width - 720), y=int(self.screen_height - 720)
        )

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = tk.Button(
            master=self.frame_left, text="Set Marker", command=self.set_marker_event
        )
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = tk.Button(
            master=self.frame_left, text="Clear Marker", command=self.clear_marker_event
        )
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.map_label = tk.Label(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = tk.OptionMenu(
            self.frame_left,
            tk.StringVar(value="OpenStreetMap"),
            "OpenStreetMap",
            "Google normal",
            "Google satellite",
            command=self.change_map,
        )
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        self.altitude_label = tk.Label(self.frame_left, text="Altitude:", anchor="w")
        self.altitude_label.grid(row=5, column=0, padx=(20, 20), pady=(10, 0))
        self.altitude_entry = tk.Entry(master=self.frame_left)
        self.altitude_entry.insert(0, "10")
        self.altitude_entry.grid(row=6, column=0, padx=(20, 20), pady=(10, 0))

        self.button_3 = tk.Button(
            master=self.frame_left,
            text="Load Waypoints",
            command=self.load_waypoints_event,
        )
        self.button_3.grid(pady=(10, 0), padx=(20, 20), row=7, column=0)

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right)
        self.map_widget.add_left_click_map_command(self.set_marker_event)
        self.map_widget.grid(
            row=1,
            rowspan=2,
            column=0,
            columnspan=3,
            sticky="nswe",
            padx=(0, 0),
            pady=(0, 0),
        )
        self.entry = tk.Entry(master=self.frame_right)
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = tk.Button(
            master=self.frame_right, text="Search", width=12, command=self.search_event
        )
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        self.marker_listbox = tk.Listbox(master=self.frame_right)
        self.marker_listbox.grid(row=0, column=2, sticky="w", padx=(12, 0), pady=12)
        self.marker_listbox.bind("<<ListboxSelect>>", self.clear_marker_from_list_event)

        self.display_table_frame = tk.Frame(master=self.frame_right_right)
        self.display_table_frame.grid(row=0, column=0, columnspan=1, sticky="nsew")

        self.display_table_scrollbar = tk.Scrollbar(
            self.display_table_frame, orient="vertical"
        )
        self.display_table_scrollbar.pack(side="right", fill="y")

        self.display_table = tk.Text(
            self.display_table_frame, yscrollcommand=self.display_table_scrollbar.set
        )
        self.display_table.pack(side="left", fill="both", expand=True)
        self.display_table_scrollbar.config(command=self.display_table.yview)

        self.map_widget.set_tile_server(
            "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
        )
        self.map_widget.set_zoom(18)
        self.map_widget.set_position(
            self.gps_lat_lon_init[0], self.gps_lat_lon_init[1], marker=False
        )

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def set_marker_event(self, event=None):
        current_position = self.map_widget.get_position()
        altitude = self.altitude_entry.get()
        if altitude:
            try:
                altitude = int(altitude)
            except ValueError:
                altitude = 10
        marker = self.map_widget.set_marker(
            current_position[0], current_position[1], altitude
        )
        self.marker_list.append(
            {
                "marker": marker,
                "position": current_position,
                "altitude": altitude,
            }
        )
        self.update_marker_listbox()

    def clear_marker_event(self):
        for marker_dict in self.marker_list:
            marker_dict["marker"].delete()
        self.marker_list.clear()
        self.update_marker_listbox()

    def clear_marker_from_list_event(self, event=None):
        selection = self.marker_listbox.curselection()
        if selection:
            index = selection[0]
            self.marker_list[index]["marker"].delete()
            del self.marker_list[index]
            self.update_marker_listbox()

    def update_marker_listbox(self):
        self.marker_listbox.delete(0, "end")
        for i in range(len(self.marker_list)):
            self.marker_listbox.insert("end", str(i + 1))
        if self.marker_list:
            self.marker_listbox.selection_set(len(self.marker_list) - 1)

        self.display_table.delete(1.0, "end")
        for i, marker_dict in enumerate(self.marker_list):
            self.display_table.insert(
                "end",
                f"Marker {i+1}: Lat: {marker_dict['position'][0]:.6f}, "
                f"Lon: {marker_dict['position'][1]:.6f}, "
                f"Altitude: {marker_dict['altitude']} m\n",
            )

    def change_map(self, new_map_type):
        if new_map_type == "OpenStreetMap":
            self.map_widget.set_tile_server(
                "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"
            )
        elif new_map_type == "Google normal":
            self.map_widget.set_tile_server(
                "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"
            )
        elif new_map_type == "Google satellite":
            self.map_widget.set_tile_server(
                "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
            )

    def load_waypoints_event(self):
        for i, marker_dict in enumerate(self.marker_list):
            print(
                f"Marker {i+1}: Lat: {marker_dict['position'][0]:.6f}, "
                f"Lon: {marker_dict['position'][1]:.6f}, "
                f"Altitude: {marker_dict['altitude']} m"
            )

    def update_socket(self, message):
        if message["header"] == "droneStatusGps":
            print(f"updating map {message}")
