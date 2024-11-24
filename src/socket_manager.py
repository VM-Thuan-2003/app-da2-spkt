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
        self.sio.on("message", self.on_message)

    def on_connect(self):
        print("Connected to Socket.IO server.")

    def on_disconnect(self):
        print("Disconnected from Socket.IO server.")

    def on_message(self, data):
        """Handle incoming messages from the server."""
        print(f"Message received: {data['data']}")
        # Call the callback to update the GUI
        self.on_message_callback(data["data"])

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

    def send_message(self, message):
        """Emit a message to the server."""
        self.sio.emit("message", {"data": message})

    def disconnect(self):
        """Disconnect the Socket.IO client."""
        self.sio.disconnect()
