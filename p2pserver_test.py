import socketserver
import socket
import threading
class ThreadTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = str(self.request.recv(1024),"ascii")
        cur_thread = threading.current_thread()
        response = bytes("{}:{}".format(cur_thread.name,data),'ascii')
        self.request.sendall(response)
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
def client(ip,port,message):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.connect((ip,port))
        sock.sendall(bytes(message,'ascii'))#bytes类，生成bytes实例
        response = str(sock.recv(1024),'ascii')#接收1024位数据
        print("Received: {}".format(response))
#ThreadingMixIn:提供Server类中process_request方法的新实现,会开启新的线程
            # ,想要让Server类实现并发处理，只用利用多重继承即可。或者直接使用已经混合好的
if __name__ == "__main__":
        Host,Port = "localhost",0
        server =ThreadedTCPServer((Host,Port),ThreadTCPRequestHandler)
        with server:
            ip,port = server.server_address
            server_thread = threading.Thread(target = server.serve_forever)
            server_thread.daemon = True  #server_thread变成后台驻留程序
            server_thread.start()
            print("Server loop running in thread:",server_thread.name)

            client(ip,port,"fuck you!1")
            client(ip,port,"fuck you!2")

            server.shutdown()