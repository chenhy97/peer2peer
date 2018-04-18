import socket
import socketserver
import threading
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("connected by:",self.client_address)
        cur_thread=threading.current_thread()
        print("Thread: ",cur_thread.name)
        while True:
            client_data = str(self.request.recv(1024),"ascii")
            print(client_data)
            sayings = input("Servers says:")
            self.request.sendall(bytes(sayings,"ascii"))

if __name__ == "__main__":
        host,port = "0.0.0.0",9999
        server = socketserver.ThreadingTCPServer((host,port),MyTCPHandler)
        server.serve_forever()
        server.shutdown()