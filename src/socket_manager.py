import socketio
from threading import Thread


class SocketManager:
    def __init__(self, on_message_callback):
        """Initialize the Socket.IO client and set up event handlers."""
        self.sio = socketio.Client()
        self.on_message_callback = on_message_callback

        # Register Socket.IO event handlers
        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)
        self.sio.on("error", self.on_error)

        # self.sio.on("message", self.on_message)
        self.sio.on("web", self.on_message)

    def on_connect(self):
        print("Connected to Socket.IO server.")

    def on_disconnect(self):
        print("Disconnected from Socket.IO server.")

    def on_error(self, data):
        print(f"Socket.IO error: {data}")

    def on_message(self, data):
        """Handle incoming messages from the server."""
        # print(f"Message received: {data}")
        # Call the callback to update the GUI
        self.on_message_callback(data)

    def start(self, server_url):
        """Start the Socket.IO client in a separate thread."""

        def run_socket_io():
            try:
                self.sio.connect(server_url)
                self.sio.wait()
            except Exception as e:
                print(f"Socket.IO connection error: {e}")

        # Start Socket.IO in a background thread
        self.thread = Thread(target=run_socket_io, daemon=True)
        self.thread.start()

    def send_message(self, message, status=None):
        """
        Send a message to the server.
        """

        stream = message["stream"]
        direction = message["direction"]
        header = message["header"]
        data = message["data"]

        self.sio.emit(
            stream,
            {"direction": direction, "header": header, "data": data, "status": status},
        )

    def send_drone(self, message):
        """Emit a message to the server."""
        self.sio.emit("drone", {"data": message})

    def disconnect(self):
        """Disconnect the Socket.IO client."""
        self.sio.disconnect()
