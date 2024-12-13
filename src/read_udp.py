import socketio
import cv2
import numpy as np
import threading


class VideoClient:
    def __init__(self, server_url, room_id, on_message_callback=None):
        self.on_message_callback = on_message_callback
        self.sio = socketio.Client()
        self.server_url = server_url
        self.room_id = room_id
        self.frame = None
        self.setup_events()

    def setup_events(self):
        @self.sio.event
        def connect():
            print("Connected to the server")
            self.sio.emit("join_room", self.room_id)

        @self.sio.on("video_frame")
        def on_video_frame(data):
            if data:
                nparr = np.frombuffer(data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if frame is not None:
                    self.frame = frame  # Save the frame to self.frame
                    self.on_message_callback(self.frame)
            else:
                self.frame = None  # If don't receive data then self.frame = None

        @self.sio.event
        def disconnect():
            print("Disconnected from server")
            cv2.destroyAllWindows()

    def connect_to_server(self):
        print("Connecting to server video...")
        self.thread = threading.Thread(target=self.sio.connect, args=(self.server_url,))
        self.thread.daemon = (
            True  # If thread is deamon is True, it will exit when main thread is over
        )
        self.thread.start()
        self.sio.wait()

    def disconnect(self):
        """Disconnect the Streaming client."""
        self.sio.disconnect()


if __name__ == "__main__":
    # Usage
    client = VideoClient("http://103.167.198.50:6001", "123456")
    client.connect_to_server()
