import socket
import json

hostname = '192.168.9.102'
port = 6666
addr = (hostname,port)
clientsock = socket.socket()
clientsock.connect(addr)
message = {"hi":"woooooooo"}
message = str(message)
clientsock.send(bytes(message, encoding='utf8'))
recvdata = clientsock.recv(1024)
print(str(recvdata,encoding='utf8'))
clientsock.close()