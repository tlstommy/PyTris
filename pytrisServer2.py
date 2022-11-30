import socket
from _thread import *
import sys

player_info = ["", ""]
def threaded_client(conn, player):
    print(f"Created thread for player {player}")
    conn.send(str.encode(f"You are player {player}"))
    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            player_info[player] = data
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = player_info[0]
                else:
                    reply = player_info[1]

                print("Received: ", data)
                print("Sending : ", reply)
            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()

server_ip = socket.gethostbyname(socket.gethostname())
port = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server_ip, port))
except socket.error as e:
    print(e)

print(f"socket created on {socket.gethostbyname(socket.gethostname())} with port: {port}\n")


s.listen(2)
print("Waiting for a connection, Server Started")

num_players = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, num_players))
    num_players += 1

s.close()