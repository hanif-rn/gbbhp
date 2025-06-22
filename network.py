import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            print(f"Connection failed: {e}")
            return None

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(4096)
            if not reply:
                raise ConnectionError("Server closed connection.")
            return pickle.loads(reply)
        except Exception as e:
            print(f"Network error: {e}")
            return None

    def getP(self):
        return self.p
