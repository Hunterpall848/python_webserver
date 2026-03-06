"""A python server created using socket."""
#Imports
import socket


class Webserver:
    """ Webserver handles creating sockets and establishing a
        propper http connection with the client.
        Returns http headers and body to the client.
    """

    def __init__(self, PORT=8080, HOST_IP="0.0.0.0"):
       
        self.HOST_IP = HOST_IP
        self.PORT = PORT

    def init_server_socket(self):
        """ init_server_socket() -> Webserver object

            Creates the server socket and sets it to listen
            on the address in __init__.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.HOST_IP, self.PORT))
        self.server_socket.listen (5)
        return self.server_socket

    def accept_client(self, server_socket):
        comm_socket, clientaddr = server_socket.accept()
        return comm_socket, clientaddr

    def handle_client(self, comm_socket: socket.socket):
        """ handle_client(comm_socket) -> Webserver object

            Recieves http request from client in the form of bytes.
            Ensures full byte collection and stable client connection before continuing.
            Parses request, splits header and body, parses header and request line.
        """
        #recieves byte data from client until entire header has arrived. Ensures entire delivery when using tcp.    
        bytebuffer = b""
        while b"\r\n\r\n" not in bytebuffer:
            bytechunk = comm_socket.recv(4096)
            bytebuffer += bytechunk
            if bytechunk == b"":
                comm_socket.close()
                return
        bytedata = bytebuffer
        header_bytes, body_bytes = bytedata.split(b"\r\n\r\n", 1) #splits bytes at end of headers to sep body from head.
        header_lines = header_bytes.decode("iso-8859-1").split("\r\n") #safer than utf-8 in this instance.
        request_line = header_lines[0]
        
        #parse header into dict object.
        headers = {}
        for line in header_lines[1:]:
            if not line:
                continue
            key, value = line.split (":", 1)
            headers[key.strip().lower()] = value.strip()
        
        #parse request line into individual variables.
        method, root_path, http_ver = request_line.split(" ")
        return headers, method, root_path, http_ver
       
    def response(self, status_line, headers, body, comm_socket):
        """ reformats and encodes the headers and sends both the header and
            the body back to the client. 
        """
        header_text = status_line + "\r\n"
        for key, value in headers.items():
            header_text += f"{key}:{value}\r\n"
        header_text += "\r\n"

        #Sending response.
        comm_socket.sendall(header_text.encode("iso-8859-1"))
        comm_socket.sendall(body)
        print(f"===> Server responded to client...")

    def close_server(self):
        self.server_socket.close()
        print("===> Server shutting down...")
       


class HTTPResponse:
    """ Handles creating the http response headers.
    """

    def __init__(self, status=200):

        self.status = status

    def http_response(self, http_ver, body, content_type):
        """ http_response(http_ver, endpoint, content, content_type) -> status_line, header (dict)
            
            Creates the http_response header and status line.
        """
        headers = {
            "Content-Type": "",
            "Content-Length": "",
            "Connection": "",
        }
        status_line = f"{http_ver} {self.status} OK"
        headers["Content-Type"] = content_type
        headers["Content-Length"] = str(len(body))
        headers["Connection"] = "close"
        return status_line, headers        
       


class Router:
    """ Routes requests to correct endpoint functions.
    """

    def __init__(self):

        self.route_map = {
            ("GET","/"): self.index
        }

    def find_route(self, method, root_path):
        route = method, root_path
        if route in self.route_map:
            return self.route_map[route]

    #valid routes
    def index(self):
        content_type = "Text/HTML"
        with open ("index.html", "rb") as index:
            body = index.read()
        return body, content_type

       
#Testing
if __name__ == "__main__":
    pass 