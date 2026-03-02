"""Access server at 127.0.0.1:8080 or localhost:8080"""
import socket


class Webserver():

    def __init__(self, PORT=8080, HOST_IP="0.0.0.0"):
       
        self.HOST_IP = HOST_IP
        self.PORT = PORT

    def init_server_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST_IP, self.PORT))
        self.server_socket.listen (5)
        return self.server_socket

    def accept_client(self, server_socket):
        comm_socket, clientaddr = server_socket.accept()
        return comm_socket, clientaddr

    def handle_client(self, comm_socket: socket.socket):
        #recieves byte data from client until entire header has arrived. Ensures entire delivery when using tcp.    
        bytebuffer = b""
        while b"\r\n\r\n" not in bytebuffer:
            bytechunk = comm_socket.recv(4096)
            bytebuffer += bytechunk
            if bytechunk == b"":
                print("===> Client Disconnected...")
                comm_socket.close()
                return
        bytedata = bytebuffer
        header_bytes, body_bytes = bytedata.split(b"\r\n\r\n", 1) #splits bytes at end of headers to sep body from head.
        header_lines = header_bytes.decode("iso-8859-1").split("\r\n") #safer than utf-8 in this instance.
        request_line = header_lines[0]
        headers = {}

        #parse header into dict object.
        for line in header_lines[1:]:
            if not line:
                continue
            key, value = line.split (":", 1)
            headers[key.strip().lower()] = value.strip()
        
        #parse request line into individual variables.
        method, root_path, http_ver = request_line.split(" ")
        return headers, method, root_path, http_ver


class Router():
    pass



if __name__ == "__main__":

    server = Webserver()
    server_socket = server.init_server_socket()
    print(f"===> Server socket initialized at host {server.HOST_IP}:{server.PORT}...")
    print(f"===> Server now running at {server.HOST_IP}:{server.PORT}...")
    #everything in the block will be reiterated when a new client connects
    while True:
        comm_socket, clientaddr = server.accept_client(server_socket)
        print(f"===> Connected to client at {clientaddr}...")
        server.handle_client(comm_socket)
