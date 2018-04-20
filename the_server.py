import socket
import os
import sys
from struct import *
import socketserver
import threading

port = 12001
host = "localhost"
server = socket.socket()
server.bind((host,port))
server.listen(5)
while True:
    client,addr = server.accept()
    buf_size = calcsize('128s128s')
    buf = client.recv(buf_size)
    if buf:
        temp_cmd,temp_file_info = unpack('128s128s',buf)
        cmd = (temp_cmd.decode('utf-8')).strip('\0')
        print(cmd)
        if cmd == 'trans':
        #print(len(cmd))
            file_info = (temp_file_info.decode('utf-8')).strip('\0')
            #example =  str(client.recv(1024),"ascii")
            with open('the_chart.txt') as file_object:
                lines = file_object.readlines()
            return_list = []
            for line in lines:
                if file_info in line:
                    return_list.append((line[20:-1].strip()).ljust(25))
            return_line = ''
            for line in return_list:
                return_line = return_line + line
            client.sendall(bytes(return_line,'ascii'))

        elif cmd == 'ls':
            with open('the_chart.txt') as file_object:
                lines = file_object.readlines()
            temp = []
            return_line = ''
            for line in lines :
                if line[0:20] not in temp:
                    return_line = return_line + line[0:20]#文件名需要小于20
                    temp.append(line[0:20])
            client.sendall(bytes(return_line,'ascii'))



