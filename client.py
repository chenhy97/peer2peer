import socket

#host = "172.19.101.14"#服务器ip
host = "localhost"
port = 9999

client = socket.socket()
client.connect((host,port))
while True:
    cmd = input("Input some msg:")
    client.sendall(bytes(cmd,"ascii"))
    data = str(client.recv(1024),"ascii")
    print(data)