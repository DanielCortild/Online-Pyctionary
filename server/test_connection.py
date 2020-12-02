import socket
import json
import time


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
            d = ""
            while True:
                last = self.client.recv(1024).decode()
                d += last
                try:
                    if d.count(".") == 1:
                        break
                except:
                    pass
            if d[-1] == ".":
                d = d[:-1]
            keys = [key for key in data.keys()]
            return json.loads(d)[str(keys[0])]
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
print(n.send({1: []}))
print(n.send({1: []}))

# Only 8 has not been tested (Update Board)!!
# 5:25:20
# https://www.youtube.com/watch?v=wDIQ17T3sRk&list=WL&index=1&t=14429s&ab_channel=TechWithTim
