import socket
import os
import sys
import struct
import _thread
from basic import *


def send_file():
	"""send a file with socket"""
	send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	send_socket.connect(ADDR1)

	file_head = struct.pack(FILEINFO_SIZE, filename.encode(), os.stat(filename).st_size)
	#I = 4s

	send_socket.send(file_head)
	with open(filename, 'rb') as file_object:
		#i = 0
		restsize = os.stat(filename).st_size	#待修改
		while True:
			filedata = file_object.read(BUF_SIZE)
			if not filedata:
				break
			if restsize >= os.stat(filename).st_size / 2:
				restsize -= BUF_SIZE
				continue
			else:
				send_socket.send(filedata)
				restsize -= BUF_SIZE

			#i += 1
			#print(i)

		print("File sending complete!")
		send_socket.close()
		print("Sending link closed.")


def server():
	"""establish a server"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(ADDR2)
	s.listen(10)
	while True:
		cfd, address = s.accept()
		buf = cfd.recv(1024)
		if not buf:
			continue
		if buf == b"get":
			send_file()
		elif buf == b"quit":
			print("Connection closed.")
			break
		else: 
			print(buf, address)
			cfd.send(buf)
		cfd.close()


if __name__ == '__main__':
	server()
