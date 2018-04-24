import socket 
import struct
import os, sys
import threading
import time
import json
from merge_file import merge_file
from list_json import rec_list
from basic import *


def rec_file(address):
	"""recieve a file with socket"""
	rec_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	rec_socket.bind(address)												######										
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

	filename = SRC + filename.decode().strip('\00')
	with open(filename, 'wb') as file_object:
		while True:
			if restsize > BUF_SIZE:
				filedata = conn.recv(BUF_SIZE)
			else:
				filedata = conn.recv(restsize)
			if not filedata:
				break
			file_object.write(filedata)

		print("File sending complete!\n")
	

def p2p_rec(address, filename, server_num, part_num):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(address)										########
	cmd_head = struct.pack(CMD_SIZE, b'get', filename.encode(), server_num, part_num)
	s.send(cmd_head)
	rec_address = s.recv(1024)
	rec_address = tuple(json.loads(rec_address.decode()))
	rec_file(rec_address)


def upload(s):
	temp_list = os.listdir(LIB)
	json_name = 'filelist_up.json'

	with open(json_name,'w') as json_obj:
		json.dump(temp_list, json_obj)

	filesize = os.stat('filelist_up.json').st_size
	file_head = struct.pack(FILEINFO_SIZE, b'temp.json',filesize)
	s.send(file_head)
	with open('filelist_up.json','rb') as file_object:
		while True:
			filedata = file_object.read(BUF_SIZE)
			if not filedata:
				print('List sending complete!')
				break
			else:
				s.send(filedata)

	os.remove(json_name)
	

def client():
	"""establish a client"""
	print("*******************************************************")
	print("Welcome to use my P2P system\n")
	print("Escape by 'quit'\n")
	print("*******************************************************")
	while True:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(ADDR1)
		buf = input("C:\\Administrator\\>").split()
		if not buf:
			continue
		if len(buf) == 1:	
			if buf[0] == "quit":
				cmd_head = struct.pack(CMD_SIZE, buf[0].encode(), b'\00', 0, 0)
				s.send(cmd_head)
				s.close()
				break
			elif buf[0] == 'upload':
				choose = input("Do you want to upload your pack? y/n ")
				if choose == 'y':
					#**************************************************************
					cmd_head = struct.pack(CMD_SIZE, buf[0].encode(), str(ADDR5).encode(), 0, 0)
					#ADDR3为客户端地址
					#**************************************************************
					s.send(cmd_head)
					upload(s)
					s.close()
				elif choose == 'n':
					pass
				else:
					print("Wrong input!")
				continue
			else:
				cmd_head = struct.pack(CMD_SIZE, buf[0].encode(), b'\00', 0, 0)
				s.send(cmd_head)
				reply = s.recv(BUF_SIZE)
				if len(reply):
					print(reply.decode())

		elif buf[0] == 'get' and len(buf) == 2:
			lib_files = os.listdir(LIB)				
			if buf[1] in lib_files:
				print("You have already had " + buf[1] + "!")
				continue
			cmd_head = struct.pack(CMD_SIZE, buf[0].encode(), buf[1].encode(), 0, 0)
			s.send(cmd_head)
			src_address = rec_list()
			if not src_address:
				print("There are no " + buf[1] + " on other servers!")
				continue 										
			server_num = len(src_address)
			tasks = []
			for part_num in range(server_num):
				new_thread = threading.Thread(target=p2p_rec,args=(tuple(src_address[part_num]), buf[1], server_num, part_num+1))   # Set up thread; target: the callable (function) to be run, args: the argument for the callable 
				new_thread.start() 
				tasks.append(new_thread)
			for task in tasks:
				task.join()
			merge_file()
		else:
			print("Wrong input!")
		time.sleep(1)
			


if __name__ == '__main__':
	client()
