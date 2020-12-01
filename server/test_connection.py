import socket
import json


class Network:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.name = name
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.sendall(self.name.encode())
            return json.loads(self.client.recv(2048).decode())
        except Exception as e:
            self.disconnect(e)

    def send(self, data):
        try:
            self.client.send(json.dumps(data).encode())
            return json.loads(self.client.recv(2048).decode())
        except socket.error as e:
            self.disconnect(e)

    def disconnect(self, msg):
        print(f"[EXCEPTION] Disconnected from server {msg}")
        # try:
        #     self.send({"10": []})
        # except:
        #     self.client.close()
        self.client.close()


n = Network("Daniel Test")
print(n.send({"0": []}))
