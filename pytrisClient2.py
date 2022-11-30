import socket, time

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote_address = "216.96.157.171"
        self.port = 8888

    def connect(self):
        try:
            self.client.connect((self.remote_address, self.port))
            return self.client.recv(4096).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(4096).decode()
        except socket.error as e:
            print(e)


c1 = Client()
c2 = Client()

time.sleep(1)

response_1 = c1.connect()
response_2 = c2.connect()

print(f"Response 1: {response_1}\n Response 2: {response_2}\n")

time.sleep(1)
while True:
    response_1 = c1.send("Message from c1")
    response_2 = c2.send("Message from c2")
    print(f"Response 1: {response_1}\n Response 2: {response_2}\n")
    time.sleep(1)