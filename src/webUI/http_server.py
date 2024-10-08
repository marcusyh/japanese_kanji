import http.server
import logging
from datetime import datetime
import os
import socketserver
import json
import argparse
import sys
import time
import socket
import fcntl
import errno
import signal

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
        
        # Set up logging
        self.log_directory = 'logs'
        os.makedirs(self.log_directory, exist_ok=True)
        self.log_filename = os.path.join(self.log_directory, f"server_log_{datetime.now().strftime('%Y-%m-%d')}.log")
        logging.basicConfig(filename=self.log_filename, level=logging.INFO, 
                            format='%(levelname)s - %(message)s')

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
        Log an arbitrary message to the log file and stdout.

        Args:
            format (str): A format string for the message to be logged.
            *args: The arguments which are merged into format using the string formatting operator.
        """
        message = f"{self.log_date_time_string()} - {self.address_string()} - {format%args}"
        logging.info(message)

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
    Run the HTTP server with singleton pattern.

    Args:
        port (int): The port number to run the server on.
        directory (str): The directory to serve files from.
    """
    lock_file = '/tmp/http_server.lock'
    
    try:
        # Try to acquire the lock file
        lock_fd = open(lock_file, 'w')
        fcntl.lockf(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        
        # Write the current process ID to the lock file
        lock_fd.write(str(os.getpid()))
        lock_fd.flush()
        
        # If we got here, we have the lock, so start the server
        handler = lambda *args, **kwargs: MyHandler(*args, directory=directory, **kwargs)
        
        try:
            with ReuseAddressTCPServer(("", port), handler) as httpd:
                logging.info(f"Serving directory '{directory}' at port {port}")
                print(f"Server started. Serving directory '{directory}' at port {port}")
                httpd.serve_forever()
        except OSError as e:
            if e.errno == 98:  # Address already in use
                print(f"Error: Port {port} is already in use. Please choose a different port.")
                logging.error(f"Port {port} is already in use.")
            else:
                raise
    
    except IOError as e:
        if e.errno == errno.EAGAIN:
            # The file is locked, which means the server is already running
            print("Server is already running.")
            logging.info("Attempted to start server, but it's already running.")
        else:
            # Some other error occurred
            raise
    finally:
        if 'lock_fd' in locals():
            lock_fd.close()
            os.remove(lock_file)  # Remove the lock file when done

def stop_server():
    """
    Stop the running server.
    """
    lock_file = '/tmp/http_server.lock'
    try:
        with open(lock_file, 'r') as f:
            content = f.read().strip()
            if not content:
                raise ValueError("Lock file is empty")
            pid = int(content)
        os.kill(pid, signal.SIGTERM)
        os.remove(lock_file)
        print("Server stopped.")
        logging.info("Server stopped.")
    except FileNotFoundError:
        print("Lock file not found. Searching for http_server.py process.")
        logging.info("Lock file not found. Searching for http_server.py process.")
        try:
            import psutil
            for proc in psutil.process_iter(['name', 'cmdline']):
                if proc.info['name'] == 'python' and any('http_server.py' in arg for arg in proc.info['cmdline']):
                    os.kill(proc.pid, signal.SIGTERM)
                    print(f"Server process (PID: {proc.pid}) stopped.")
                    logging.info(f"Server process (PID: {proc.pid}) stopped.")
                    return
            print("No running http_server.py process found.")
            logging.info("No running http_server.py process found.")
        except ImportError:
            print("psutil module not found. Unable to search for server process.")
            logging.error("psutil module not found. Unable to search for server process.")
    except ProcessLookupError:
        print("Server process not found. Removing lock file.")
        os.remove(lock_file)
        logging.info("Server process not found. Lock file removed.")
    except ValueError as e:
        print(f"Error reading lock file: {e}")
        logging.error(f"Error reading lock file: {e}")
        os.remove(lock_file)
        logging.info("Invalid lock file removed.")

def restart_server(port, directory):
    """
    Restart the server.

    Args:
        port (int): The port number to run the server on.
        directory (str): The directory to serve files from.
    """
    stop_server()
    time.sleep(2)  # Wait a bit longer for the server to fully stop and release the port
    run_server(port, directory)

if __name__ == "__main__":
    web_server_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Simple HTTP Server with custom features")
    parser.add_argument('-p', '--port', type=int, default=8000, help="Port to run the server on")
    parser.add_argument('-d', '--directory', type=str, default=os.path.join(web_server_dir, 'webUI'), help="Directory to serve")
    parser.add_argument('-s', '--stop', action='store_true', help="Stop the running server")
    parser.add_argument('-r', '--restart', action='store_true', help="Restart the server")
    args = parser.parse_args()

    if args.stop:
        stop_server()
    elif args.restart:
        restart_server(args.port, args.directory)
    else:
        run_server(args.port, args.directory)
