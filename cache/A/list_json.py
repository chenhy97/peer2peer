import json
import struct
import socket
import os, sys
from basic import *

LIB = 'lib//'
current_address = ADDR3

lib_files = os.listdir(LIB)

def send_list(need_file):

	filename = 'filelist.json'
	with open(filename) as file_obj:
		files = json.load(file_obj)

	if need_file in files.keys():
		with open('temp.json', 'w') as file_obj:
			json.dump(files[need_file], file_obj)
	else:
		with open('temp.json', 'w') as file_obj:
			json.dump([], file_obj)

	filesize = os.stat('temp.json').st_size
	send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	send_socket.connect(ADDR2)									#######
	filename = filename + '^' + 'temp.json'
	file_head = struct.pack(FILEINFO_SIZE, filename.encode(), filesize)
	#I = 4s

	send_socket.send(file_head)
	with open('temp.json', 'rb') as file_object:
		#i = 0
		sendsize = 0	#待修改
		while True:
			filedata = file_object.read(BUF_SIZE)
			if not filedata:
				print("List sending complete!")				
				break
			else:
				send_socket.send(filedata)
	send_socket.close()


def rec_list():
	"""recieve a file with socket"""
	rec_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	rec_socket.bind(ADDR2)
	rec_socket.listen(10)
	print("Loading...\n")

	conn, addr = rec_socket.accept()
	print("Link complete!\n")

	file_head = conn.recv(struct.calcsize(FILEINFO_SIZE))
	filename, filesize = struct.unpack(FILEINFO_SIZE, file_head)
	
	#print(filename, filesize)
	#print(filename, len(filename), type(filename))
	#print(filesize)
	
	restsize = filesize
	print("Recieving...\n")

	filename = filename.decode().strip('\00')
	with open(filename, 'wb') as file_object:
		while True:
			if restsize > BUF_SIZE:
				filedata = conn.recv(BUF_SIZE)
			else:
				filedata = conn.recv(restsize)
			if not filedata:
				break
			file_object.write(filedata)

		print("List sending complete!\n")

	with open(filename) as file_obj:
		files = json.load(file_obj)
	return files


if __name__ == '__main__':
    send_list("bilibili")

