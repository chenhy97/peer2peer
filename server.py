import socket
import socketserver
import threading
#host = "0.0.0.0"#广播报文


port = 9999
host = "localhost"
server = socket.socket()
server.bind((host,port))
server.listen(5)#监听是否有客户端
print("waiting for connection")
while True:
    for_client,addr = server.accept()#有客户端，建立相应套接字
    print("connected",addr)
    while True:
        data = str(for_client.recv(1024),"ascii")
        print(data)
        anwser = "I recived your input"
        for_client.sendall(bytes(anwser,"ascii"))
