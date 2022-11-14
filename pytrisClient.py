import json,sys,socket,os

class Client:
    def __init__(self,serverAddress,serverPort,recvPort):
        self.port = serverPort
        self.recvPort = recvPort
        self.serverAddress = serverAddress
        

    #create a new client socket
    def createClientSocket(self):
        self.clientSocket = socket.socket()
        self.clientSocket.connect((self.serverAddress,self.port))
    #send the json data
    def sendData(self,jsonData):
        #encode data and send
        self.clientSocket.send(json.dumps(jsonData).encode())
    

    def receiveData(self):
        #decode json 
        opponentJson = json.loads(self.clientSocket.recv(4096).decode())
        if(opponentJson == "gameOver"):
            print("Gameover")
            return -1
        opponentJson["currentGrid"] = list(opponentJson["currentGrid"])
        return opponentJson
        
#serverIP = input("please enter the server IP: ")


#create a new client for the server at serverIP:8888, and open on port 25000 for reciveing

    
