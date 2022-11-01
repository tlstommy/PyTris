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
        print("SENDDATA:")
        print(jsonData)
        #encode data and send
        self.clientSocket.send(json.dumps(jsonData).encode())
    

    def receiveData(self):
        #decode json 
        opponentJson = json.loads(self.clientSocket.recv(4096).decode())
        return opponentJson
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
        
    

#serverIP = input("please enter the server IP: ")


#create a new client for the server at serverIP:8888, and open on port 25000 for reciveing

    
