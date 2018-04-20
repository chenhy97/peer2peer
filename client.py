import socket
from  struct import *
import os

#host = "172.19.101.14"#服务器ip
host = "localhost"
port = 12001

client = socket.socket()
client.connect((host,port))
while True:
    filename = input("Input some msg:")
    client.sendall(bytes(filename,"ascii"))
    while True:
        file_info_size = calcsize('128sl')
        file_buf = client.recv(file_info_size)
        if file_buf:
            file_name,file_size=unpack('128sl',file_buf)
            file_name_real = filename
            new_file = os.path.join('./file','new_' + file_name_real)
            print(new_file,file_size)

            received_size = 0
            fp = open(new_file,'wb')
            print("writing")
            while not received_size == file_size:
                if(file_size - received_size > 1024):
                    data = client.recv(1024)
                    received_size = received_size + len(data)
                else:
                    data = client.recv(file_size - received_size)
                    received_size = file_size
                fp.write(data)
            fp.close()
            print("OK")
        else:
            print(file_buf)
        break;

    anwser = str(client.recv(1024),"ascii")
