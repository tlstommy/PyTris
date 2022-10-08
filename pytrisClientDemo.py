import json,sys,socket,os

import numpy
import numpy.random

#just for demo idrk how big a tetris board is. 0 is a free space 1 is a block
def genRandomBoard():
    return numpy.random.randint(2,size=(5, 3))

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
        opponentJson = json.loads(self.clientSocket.recv(1024).decode())
        try:
            opponentUsername = opponentJson["username"]
            print(f"\n{opponentUsername}'s Board:\n")

            print(opponentJson["currentGrid"][0])
            print(opponentJson["currentGrid"][1])
            print(opponentJson["currentGrid"][2])
            print(opponentJson["currentGrid"][3])
            print(opponentJson["currentGrid"][4])

        #its an error message
        except TypeError as e:
            print("Type Error")
            print(opponentJson)
        
    

serverIP = input("please enter the server IP: ")


#create a new client for the server at serverIP:8888, and open on port 25000 for reciveing
client = Client(serverIP,8888,recvPort=25000)



while True:
    
    #get players username
    playerName = input("\n\nPlease enter your username: ")
    
    #build json data
    jsonData = {
                "username":playerName, 
                "ip":socket.gethostbyname(socket.gethostname()),
                "recvPort":client.recvPort,
                "currentGrid":genRandomBoard().tolist(),                
                }

    #send json data to the server over socket     
    client.createClientSocket();client.sendData(jsonData)

    #listen for data from the server
    client.receiveData()
    
