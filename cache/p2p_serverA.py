import socket
import os
import sys
import struct
import socketserver
import _thread
from basic import *


def p2p_send_file(server_num=1, part_num=1):
	"""send a file with socket by P2P"""
	global filename
	send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	send_socket.connect(ADDR4)

	
	filesize = os.stat(filename).st_size
	sending_start = (part_num - 1) / server_num * filesize
	sending_end = part_num / server_num * filesize
	part_filename = str(part_num) + '^' + filename
	file_head = struct.pack(FILEINFO_SIZE, part_filename.encode(), filesize)
	#I = 4s

	send_socket.send(file_head)
	with open(filename, 'rb') as file_object:
		#i = 0
		sendsize = 0	#待修改
		while True:
			filedata = file_object.read(BUF_SIZE)
			if not filedata:
				print("File sending complete!")				#这里一定要有不然会有玄学错误
				break
			if (sendsize >= sending_start and sendsize < sending_end):
				send_socket.send(filedata)
			sendsize += BUF_SIZE

			#i += 1
			#print(i)

		send_socket.close()
		print("Sending link closed.")


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
            cmdname, filename, server_num, part_num= struct.unpack(CMD_SIZE, cmd_head)
            cmdname = cmdname.decode().strip('\00')
            filename = filename.decode().strip('\00')
            if cmdname == 'get':
                p2p_send_file(server_num, part_num)
            elif cmdname == "quit":
                print("Connection closed.")
                break
            else: 
                print(buf, self.client_address)



if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(ADDR3, Server) #实现了多线程的socket通话
    server.serve_forever()#不会出现在一个客户端结束后，当前服务器端就会关闭或者报错，而是继续运行，与其他的客户端继续进行通话。
