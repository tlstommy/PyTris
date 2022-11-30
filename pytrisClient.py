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

# Opponent Class for keeping track of the Opponent's board
# Currently a placeholder for later socket integration


class Opponent(object):
    def __init__(self, name, locked_pos={}):
        self.name = name
        self.locked_pos = locked_pos

#create a new client for the server at serverIP:8888, and open on port 25000 for reciveing
    
# PlayerInfo class used for data encoding and decoding over socket
# Holds information such as username, ip, and locked positions formatted through
# a json object
class PlayerInfo(object):
    def __init__(self, name, IP, grid, locked_pos = {}):
        self.username = name
        self.ip = IP
        self.locked_pos = []
        self.game_start = False
        self.game_end = False
        self.send_garbage = 0

        # Formatting dictionary into a 1D array for json enc
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_pos:
                    c = locked_pos[(j,i)]
                    self.locked_pos.append(c)
                else:
                    self.locked_pos.append((0,0,0))

    # Updating the 1D array of locked positions
    def update(self, grid, locked_pos = {}):
        counter = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_pos:
                    c = locked_pos[(j,i)]
                    self.locked_pos[counter] = (c)
                else:
                    self.locked_pos[counter] = (0,0,0)
                counter += 1
 
    # JSON encoding used to send data to client over socket server
    def json_enc(self):
        return json.dumps(self, indent = 4, default = lambda o: o.__dict__)

    def json_dec(self, json_string):
        self = json.loads(json_string)

    # JSON decoding used to recieve opponent data and decode into grid
    def grid_dec(self, grid, opponent):
        counter = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                c = self.locked_pos[counter]
                if (c != (0,0,0)):
                    opponent.locked_pos[(j,i)] = (c)
                counter += 1

    def send_garbage(self, lines):
        self.send_garbage = lines
        return