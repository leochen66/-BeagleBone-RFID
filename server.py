import socket
import json

hostname = '192.168.9.102'
port = 6666
addr = (hostname,port)
srv = socket.socket()
srv.bind(addr)
srv.listen(5)
print("waitting connect")
while True:
	connect_socket, client_addr = srv.accept()
	# print(client_addr)
	recieve = connect_socket.recv(1024)
	recieve = str(recieve,encoding='utf8').replace("'", '"')
	data = json.loads(recieve)
	print(data)
	connect_socket.send(bytes('Success', encoding='utf8'))
connect_socket.close()