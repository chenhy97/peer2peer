import socket
import os
import sys
from struct import *
import socketserver
import threading
#host = "0.0.0.0"#广播报文
def fix_address(string):
    length = int(len(string) / 25)
    print(length)
    answer = []
    for i in range(length):
        apart = string[25 * i:25 * i + 25]
        print(apart)
        address = apart[0:16].strip()
        port = int(apart[16:-1].strip())
        the_union = (address,port)
        answer.append(the_union)
    return answer

#def ask_server_forhelp(file_name):
def ask_server_forhelp():
    port = 12001
    host = 'localhost'
    client = socket.socket()
    client.connect((host,port))

    cmd = input("what do you want?")
    if cmd == 'trans':
        file_name = input("What do you need?")
        packege = calcsize('128s128s')
        cmdhead = pack('128s128s',cmd.encode('utf-8'),file_name.encode('utf-8'))
        client.sendall(cmdhead)



        file_addresses = str(client.recv(1024),'ascii')
        print(file_addresses)
        address_list = fix_address(file_addresses)
        client.close()
        return (file_name,address_list)
    #else cmd == 'ls':
def data_upload():



def p2p_upload():
    port = 9998
    host = 'localhost'
    server = socket.socket()
    server.bind((host, port))
    server.listen(10)  # 监听是否有客户端
    print("waiting for connection")
    while True:
        for_client, addr = server.accept()  # 有客户端，建立相应套接字
        print("connected", addr)

        while True:
            filepath = str(for_client.recv(1024), "ascii")
            print(filepath)
            # anwser = "I recived your input"
            if os.path.isfile(filepath):
                statinfo = os.stat(filepath)
                size = statinfo.st_size  # basename 返回文件名字，而无路径
                file_info = calcsize('128sl')
                filehead = pack('128sl', filepath.encode('utf-8'), size)  # 我们可以使用128sl这样的方法表示128个c
                # har型和一个long型，或者2i表示两个int整型.
                for_client.sendall(filehead)
                print("file size is:", size)
                fileop = open(filepath, 'rb')
                while True:
                    data = fileop.read(1024)
                    if not data:
                        print("finished sending")
                        break
                    for_client.sendall(data)
            else:
                anwser = "no such file,input again"
                for_client.sendall(bytes(anwser, "ascii"))
    server.shutdown()
def p2p_receive(client_union):
    # host = "172.19.101.14"#服务器ip
    host = 'localhost'
    port = 9998
    client = socket.socket()
    client.connect(client_union[1][0])
    while True:
        client.sendall(bytes(client_union[0], "ascii"))
        while True:
            file_info_size = calcsize('128sl')
            file_buf = client.recv(file_info_size)
            if file_buf:
                file_name1, file_size = unpack('128sl', file_buf)
                file_name_real = client_union[0]
                new_file = os.path.join('./file', 'new_' + file_name_real)
                print(new_file, file_size)

                received_size = 0
                fp = open(new_file, 'wb')
                print("writing")
                while not received_size == file_size:
                    if (file_size - received_size > 1024):
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
            break

        anwser = str(client.recv(1024), "ascii")

upload_or_receive = input("you want to upload or receive: ")

if upload_or_receive == 'upload':
    data_upload()
    p2p_upload()
else:
    #file_name = input("please input the filename you want to get:")
    address_union = ask_server_forhelp()
    p2p_receive(address_union)