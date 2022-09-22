import json,sys,socket

import numpy
import numpy.random

#just for demo idrk how big a tetris board is. 0 is a free space 1 is a block
def genRandomBoard():
    return numpy.random.randint(2,size=(3, 3))

class Client:
    def __init__(self,serverAddress,serverPort,recvPort):
        self.port = serverPort
        self.recvPort = recvPort
        self.serverAddress = serverAddress
    def createClientSocket(self):
        self.clientSocket = socket.socket()
        self.clientSocket.connect((self.serverAddress,self.port))
    def sendData(self,jsonData):
        #encode data and send
        self.clientSocket.send(json.dumps(jsonData).encode())
    def receiveData(self):

        print("\nOPPONENT DATA:")
        print(self.clientSocket.recv(1024).decode())
    

serverIP = input("please enter the server IP: ")


client = Client(serverIP,8888,recvPort=25000)



while True:
    
    playerName = input("\n\nPlease enter your username: ")
    jsonData = {
                "username":playerName, 
                "ip":socket.gethostbyname(socket.gethostname()),
                "recvPort":client.recvPort,
                "currentGrid":genRandomBoard().tolist(),                
                }
    client.createClientSocket()
    client.sendData(jsonData)
    client.receiveData()
    
