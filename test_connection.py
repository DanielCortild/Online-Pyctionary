import socket
import json


class Network:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = "188.166.107.89"
        self.addr = ("localhost", 1287)
        self.name = name
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.sendall(self.name.encode())
            print(self.client.recv(1024).decode())
        except Exception as e:
            self.disconnect(e)

    def send(self, data):
        try:
            self.client.send(json.dumps(data).encode())
            d = ""
            while d.count(".") == 0:
                d += self.client.recv(1024).decode()
            return json.loads(d.replace(".", ""))
        except Exception as e:
            self.disconnect(e)

    def disconnect(self, msg):
        print(f"[EXCEPTION] Disconnected because {msg}")
        self.client.close()


if __name__ == "__main__":
    n = Network("Daniel Test")
    print(n.send({10: []}))
