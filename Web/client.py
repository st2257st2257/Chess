import socket
import json

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(9)
client_sock.connect(('46.138.245.249', 11111))
print(9)
client_sock.sendall(json.dumps([8, [472]]).encode())
print(9)
data = json.loads(client_sock.recv(1024))
print(9)
client_sock.close()
print('Received', repr(data))
