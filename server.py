import socket
from _thread import *
import sys


server = "26.188.24.15"   # <wolly ip>
port = 5555

datasize = 2048
max_connections = 4

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(max_connections)
print("Waiting for connection, server started")

def threaded_client(conn):
    conn.send(str.encode("connected"))
    while True:
        try:
            data = conn.recv(datasize)
            reply = data.decode("utf-8")

            if not data:
                print("disconnected")
                break
            else:
                print("received: ", reply)
                print("sending :", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, ))