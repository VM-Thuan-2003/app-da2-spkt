import osmnx as ox
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class Map:
    def __init__(self, frame, send_callback):
        self.frame = frame
        self.send_callback = send_callback

        self.screen_width = frame.winfo_screenwidth()
        self.screen_height = frame.winfo_screenheight()

        self.payload_socket_map = {
            "current": {"lat": "", "lon": "", "alt": ""},
            "home": {"lat": "", "lon": "", "alt": ""},
        }

        # Default location (Hanoi, Vietnam)
        self.location = [21.028511, 105.804817]

        # Initialize Matplotlib figure and canvas
        self.fig = None
        self.canvas = None

        # Display the map
        self.display_map()

    def display_map(self):
        """Displays the map using osmnx and embeds it in the Tkinter frame."""
        # Fetch map data for the specified location
        location_name = "Hanoi, Vietnam"
        graph = ox.graph_from_place(location_name, network_type="all")

        # Create the plot
        self.fig, ax = ox.plot_graph(graph, show=False, close=True)

        # Embed the plot in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def update_socket(self, message):
        """Handles socket message updates (to be implemented)."""
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        if self.fig:
            plt.close(self.fig)
