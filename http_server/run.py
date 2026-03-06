"""Runs a server using TCP and websocket http."""
#Imports
from http_server import Webserver, Router, HTTPResponse


#Main server process
def main():

    #Instantiate all classes.
    webserver: Webserver = Webserver()
    router: Router = Router()
    http_response: HTTPResponse = HTTPResponse()

    #Initiate server socket on port 8080.
    server_socket = webserver.init_server_socket()
    print(f"===> Server socket initialized at host {webserver.HOST_IP}:{webserver.PORT}...")
    print(f"===> Server now running at {webserver.HOST_IP}:{webserver.PORT}...")

    #Server loop.
    while True:
        try:
            #Checks to make sure the client didnt disconnect.
            response_check = webserver.accept_client(server_socket)
            if response_check != None:
                comm_socket, clientaddr = response_check
                print(f"===> Connected to client at {clientaddr}...")
            else:
                disconnect = response_check
                print("===> Client Disconnected...")

            #Path validation.
            headers, method, root_path, http_ver = webserver.handle_client(comm_socket)
            route = method, root_path
            if route in router.route_map.keys():
                handler = router.find_route(method, root_path)
            else:
                print("Error 404: Path not found...")
                comm_socket.close()
                continue

            #Build response for client.
            body, content_type = handler()
            status_line, headers = http_response.http_response(http_ver, body, content_type)
            webserver.response(status_line, headers, body, comm_socket)
        except:
            #Shutting down server.
            KeyboardInterrupt
            webserver.close_server()
            break

   
if __name__ == "__main__":
    main()