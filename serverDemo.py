import json,sys,socket


class Server:
    def __init__(self,port):
        self.port = port
        self.player1 = None
        self.player2 = None
        #ids for now are just username+ip
        self.player1ID = None
        self.player2ID = None
    def createServerSocket(self):
        self.serverSocket = socket.socket()
        self.serverSocket.bind(('',self.port))
        self.serverSocket.listen(20)
        print(f"socket created on {socket.gethostbyname(socket.gethostname())} with port: {self.port}\n")
        while True:
            self.listenForConn()
            #break
        
    def listenForConn(self):
        self.serverSocket.listen(2)
        c,addr = self.serverSocket.accept()
        #decode json
        decodedJson = json.loads(c.recv(1024).decode())

        print("\n---=INBOUND MESSAGE=---")
        print("CLIENT ADDRESS  :",addr[0])
        print("CLIENT PORT     :",decodedJson.get("recvPort"))
        print("CLIENT USERNAME :",decodedJson.get("username"))
        print("CLIENT BOARD:")
        print(decodedJson.get("currentGrid")[0])
        print(decodedJson.get("currentGrid")[1])
        print(decodedJson.get("currentGrid")[2])

        self.storePlayerData(decodedJson,c)

    def storePlayerData(self,jsonData,c):
        currentPlayerID = (str(jsonData.get("username")+"@"+jsonData.get("ip")))
        #store player data for 2 people
        if self.player1 == None or self.player1ID == currentPlayerID:
            self.player1 = jsonData
            self.player1ID = currentPlayerID
            try:
                self.sendData(self.player2,c)
            except AttributeError as e:
                pass
        elif self.player2 == None or self.player2ID == currentPlayerID:
            self.player2 = jsonData
            self.player2ID = currentPlayerID
            try:
                self.sendData(self.player1,c)
            except AttributeError as e:
                pass
        else:
            print("MAX PLAYERS REACHED")
            self.sendData("ERROR: GAME IS FULL!",c)
            return 0
    #send data back to a client
    def sendData(self, playerJsonData,c):
        print(playerJsonData)
        c.send(json.dumps(playerJsonData).encode())
        return 0   
    def sendError(self, errorMsg,c):
        c.send(errorMsg.encode())
        return 0   
            

server = Server(8888)

server.createServerSocket()

