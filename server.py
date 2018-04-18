import socket
import socketserver
host = "localhost"
ip = 9999
server = socket.socket()
server.bind((host,ip))
server.listen(5)
print("waiting for connection")
while True:
    for_client,addr = server.accept()
    print("connected",addr)
    while True:
        data = str(for_client.recv(1024),"ascii")
        print(data)
        anwser = "I recived your input"
        for_client.sendall(bytes(anwser,"ascii"))
