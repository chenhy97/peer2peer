import socket
import os
import sys
from struct import *
import socketserver
import threading
#host = "0.0.0.0"#广播报文


port = 9999
host = "localhost"
server = socket.socket()
server.bind((host,port))
server.listen(10)#监听是否有客户端
print("waiting for connection")
while True:
    for_client,addr = server.accept()#有客户端，建立相应套接字
    print("connected",addr)

    while True:
        filepath = str(for_client.recv(1024),"ascii")
        print(filepath)
       # anwser = "I recived your input"
        if  os.path.isfile(filepath):
            statinfo = os.stat(filepath)
            size = statinfo.st_size#basename 返回文件名字，而无路径
            file_info = calcsize('128sl')
            filehead = pack('128sl',filepath.encode('utf-8'),size)#我们可以使用128sl这样的方法表示128个c
                                                                 # har型和一个long型，或者2i表示两个int整型.
            for_client.sendall(filehead)
            print("file size is:",size)
            fileop = open(filepath,'rb')
            while True:
                data = fileop.read(1024)
                if not data:
                    print("finished sending")
                    break
                for_client.sendall(data)
        else:
            anwser = "no such file,input again"
            for_client.sendall(bytes(anwser,"ascii"))
server.shutdown()