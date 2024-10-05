import http.server
import socketserver
import json
import os
import argparse
import sys
import time
import socket

class MyHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler extending SimpleHTTPRequestHandler.
    
    This handler adds functionality to serve a list of markdown files
    and provides custom logging.
    """

    def __init__(self, *args, directory=None, **kwargs):
        """
        Initialize the handler with a specific directory to serve files from.

        Args:
            *args: Variable length argument list.
            directory (str): The directory to serve files from.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        """
        Handle GET requests.

        If the path is '/file_list', return a JSON list of markdown files.
        Otherwise, delegate to the parent class method.
        """
        if self.path == '/file_list':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data_dir = os.path.join(self.directory, 'data')
            file_list = [f for f in os.listdir(data_dir) if f.endswith('.md')]
            self.wfile.write(json.dumps(file_list).encode())
        else:
            super().do_GET()

    def log_message(self, format, *args):
        """
        Log an arbitrary message to stdout.

        Args:
            format (str): A format string for the message to be logged.
            *args: The arguments which are merged into format using the string formatting operator.
        """
        print(f"{self.log_date_time_string()} - {self.address_string()} - {format%args}")

class ReuseAddressTCPServer(socketserver.TCPServer):
    """
    A TCPServer subclass that sets SO_REUSEADDR on the server socket.
    
    This allows the server to rebind to a previously used address, useful
    for rapid restarts of the server.
    """

    def server_bind(self):
        """
        Bind the socket to the server address with the SO_REUSEADDR option set.
        """
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

def run_server(port, directory):
    """
    Run the HTTP server with retry logic for port conflicts.

    Args:
        port (int): The port number to run the server on.
        directory (str): The directory to serve files from.
    """
    handler = lambda *args, **kwargs: MyHandler(*args, directory=directory, **kwargs)
    
    retries = 5
    while retries > 0:
        try:
            with ReuseAddressTCPServer(("", port), handler) as httpd:
                print(f"Serving directory '{directory}' at port {port}")
                httpd.serve_forever()
        except OSError as e:
            if e.errno == 98:  # Address already in use
                print(f"Port {port} is in use. Retrying in 2 seconds...")
                time.sleep(2)
                retries -= 1
            else:
                raise
        else:
            break
    else:
        print(f"Failed to start server after {5-retries} attempts. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple HTTP Server with custom features")
    parser.add_argument('-p', '--port', type=int, default=8000, help="Port to run the server on")
    parser.add_argument('-d', '--directory', type=str, default=f'{os.getcwd()}/html', help="Directory to serve")
    args = parser.parse_args()

    run_server(args.port, args.directory)
