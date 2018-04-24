import socketserver
import struct
import os, sys
from list_json import send_list
from server import send_file
from basic import *
import json


def update_the_json(update_address):
    used_json = 'filelist.json'
    update_json = "temp.json"
    with open(used_json) as f_obj:
        used_dic = json.load(f_obj)

    with open(update_json) as f_obj:
        update_list = json.load(f_obj)

    for update_filename in update_list:
        if update_filename in used_dic.keys():
            if list(update_address) not in used_dic[update_filename]:
                used_dic[update_filename].append(update_address)
        else:
            used_dic[update_filename] = []
            used_dic[update_filename].append(update_address)

    for filename, address in used_dic.items():
        if update_address in address:
            if filename not in update_list:
                used_dic[filename].remove(update_address)

    with open(used_json, 'w') as f_obj:
        json.dump(used_dic,f_obj)

    os.remove(update_json)


#定义一个类，继承socketserver.BaseRequestHandler
class Server(socketserver.BaseRequestHandler):
    """Threading Server"""
     
    def handle(self):
    #打印客户端地址和端口
        print('New connection:', self.client_address)
    #循环
        while True:
        #接收客户发送的数据
            cmd_head = self.request.recv(struct.calcsize(CMD_SIZE))
            if not cmd_head:
                break
            cmdname, argname, temp1, temp2 = struct.unpack(CMD_SIZE, cmd_head)
            cmdname = cmdname.decode().strip('\00')
            argname = argname.decode().strip('\00')
            if cmdname == 'get':
                send_list(argname)
            elif cmdname == "quit":
                print("Connection closed.")
                break
            elif cmdname == 'upload':         
                json_head = self.request.recv(struct.calcsize(FILEINFO_SIZE))
                json_name,json_size = struct.unpack(FILEINFO_SIZE, json_head)

                restsize = json_size
                print("Recieving...\n")

                json_name = json_name.decode().strip('\00')
                with open(json_name, 'wb') as json_obj:
                    while True:
                        if restsize > BUF_SIZE:
                            filedata = self.request.recv(BUF_SIZE)
                        else:
                            filedata = self.request.recv(restsize)
                        if not filedata:
                            break
                        json_obj.write(filedata)
                    print("File sending complete!\n")
                
                argname = tuple(eval(argname))
                update_the_json(argname)
                print("upload complete!\n")
            else: 
                print(cmdname, self.client_address)
                self.request.send(cmdname.encode())


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(ADDR1, Server) #实现了多线程的socket通话
    server.serve_forever()#不会出现在一个客户端结束后，当前服务器端就会关闭或者报错，而是继续运行，与其他的客户端继续进行通话。