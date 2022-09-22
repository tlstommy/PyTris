import json,sys,socket

class Server:
    def __init__(self,port):
        self.port = port
    def createServerSocket(self):
        self.serverSocket = socket.socket()
        self.serverSocket.bind(('',self.port))
        self.serverSocket.listen(20)
        print(f"socket created on {socket.gethostbyname(socket.gethostname())} with port: {self.port}\n")
        self.listenForConn()
    def listenForConn(self):
        self.serverSocket.listen(2)
        content, addr = self.serverSocket.accept()
        #decode json
        decodedJson = json.loads(content.recv(1024).decode())\

        print("\n---=INBOUND MESSAGE=---")
        print("CLIENT ADDRESS  :",addr[0])
        print("CLIENT PORT     :",decodedJson.get("recvPort"))
        print("CLIENT USERNAME :",decodedJson.get("username"))
        print("CLIENT BOARD:")
        print(decodedJson.get("currentGrid")[0])
        print(decodedJson.get("currentGrid")[1])
        print(decodedJson.get("currentGrid")[2])

        
            

server = Server(8888)

server.createServerSocket()

