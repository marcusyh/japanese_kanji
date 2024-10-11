import http.server
import logging
from logging import handlers
from datetime import datetime
import os
import socketserver
import json
import argparse
import urllib.parse
import time
import socket
import fcntl
import errno
import signal
import config


def init_logger(log_directory):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory, exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    log_filename = os.path.join(log_directory, f"{current_time}.log")

    log_level = logging.INFO
    logHandler = handlers.TimedRotatingFileHandler(log_filename, when='D', interval=1, backupCount=60)

    logHandler.setFormatter(logging.Formatter('[%(asctime)s] - [%(levelname)s] - %(pathname)s:%(lineno)d - %(message)s'))

    """
    logging.basicConfig(filename=log_filename, level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    """
    logging.root.addHandler(logHandler)
    logging.root.setLevel(log_level)



class MyHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler extending SimpleHTTPRequestHandler.
    
    This handler adds functionality to serve a list of markdown files
    and provides custom logging.
    """

    wikt_files = {}  # 用于存储维基词典文件列表

    def __init__(self, *args, directory=None, **kwargs):
        """
        Initialize the handler with a specific directory to serve files from.

        Args:
            *args: Variable length argument list.
            directory (str): The directory to serve files from.
            **kwargs: Arbitrary keyword arguments.
        """
        self.kanji_wikt_dir = os.path.join(directory, config.KANJI_WIKT_DIR)
        self.pron_list_dir = os.path.join(directory, config.PRON_LIST_DIR)
        self.words_list_file = os.path.join(directory, config.WORDS_LIST_FILE)

        super().__init__(*args, directory=directory, **kwargs)
        
        if not MyHandler.wikt_files:
            self.load_wikt_files()

    def load_wikt_files(self):
        for filename in os.listdir(self.kanji_wikt_dir):
            if filename.endswith('.html'):
                kanji = filename[:-5]  # 移除 .html 后缀
                MyHandler.wikt_files[kanji] = kanji 

    def do_GET(self):
        """
        Handle GET requests.
        """
        handlers = {
            '/pron_list': self.handle_pron_list,
            '/kanji_wikt': self.handle_kanji_wikt,
            '/words_list': self.handle_words_list
        }

        for prefix, handler in handlers.items():
            if self.path.startswith(prefix):
                return handler()

        super().do_GET()

    def handle_pron_list(self):
        if self.path == '/pron_list':
            self.send_json_response(sorted([f.split('.')[0] for f in os.listdir(self.pron_list_dir) if f.endswith('.md')]))
        else:
            self.serve_file(self.pron_list_dir, '.md', 'text/markdown')

    def handle_kanji_wikt(self):
        if self.path == '/kanji_wikt':
            self.send_json_response(MyHandler.wikt_files)
        else:
            self.serve_file(self.kanji_wikt_dir, '.html', 'text/html')

    def handle_words_list(self):
        self.serve_file(os.path.dirname(self.words_list_file), '.json', 'application/json', self.words_list_file)

    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def serve_file(self, directory, extension, content_type, specific_file=None):
        if specific_file:
            file_path = specific_file
        else:
            path_without_query = self.path.split('?')[0]
            filename = path_without_query.replace('//', '/').split('/')[-1]
            filename = f'{urllib.parse.unquote(filename)}{extension}'
            file_path = os.path.join(directory, filename)

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(content.encode())
        else:
            self.send_error(404, "File not found")

    def log_message(self, format, *args):
        """
        Log an arbitrary message to the log file.

        Args:
            format (str): A format string for the message to be logged.
            *args: The arguments which are merged into format using the string formatting operator.
        """
        message = f"{self.address_string()} - {format%args}"
        logging.info(message)


class ServerManager:
    def __init__(self, port, directory):
        self.port = port
        self.directory = directory
        self.lock_file = config.LOCK_FILE

    class ReuseAddressTCPServer(socketserver.TCPServer):
        def server_bind(self):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(self.server_address)

    def run(self):
        try:
            with open(self.lock_file, 'w') as lock_fd:
                fcntl.lockf(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                lock_fd.write(str(os.getpid()))
                lock_fd.flush()
                
                self._start_server()
        except IOError as e:
            if e.errno == errno.EAGAIN:
                logging.info("Server is already running.")
            else:
                raise
        finally:
            self._cleanup()

    def _start_server(self):
        handler = lambda *args, **kwargs: MyHandler(*args, directory=self.directory, **kwargs)
        try:
            with self.ReuseAddressTCPServer(("", self.port), handler) as httpd:
                self._log_server_start()
                httpd.serve_forever()
        except OSError as e:
            if e.errno == 98:  # Address already in use
                self._log_port_in_use()
            else:
                raise

    def stop(self):
        try:
            pid = self._get_pid_from_lock_file()
            os.kill(pid, signal.SIGTERM)
            os.remove(self.lock_file)
            logging.info("Server stopped.")
        except FileNotFoundError:
            self._stop_by_process_name()
        except ProcessLookupError:
            self._handle_process_not_found()
        except ValueError as e:
            self._handle_invalid_lock_file(e)

    def restart(self):
        self.stop()
        time.sleep(2)  # Wait for the server to fully stop
        self.run()

    def _get_pid_from_lock_file(self):
        with open(self.lock_file, 'r') as f:
            content = f.read().strip()
            if not content:
                raise ValueError("Lock file is empty")
            return int(content)

    def _stop_by_process_name(self):
        logging.info("Lock file not found. Searching for http_server.py process.")
        try:
            import psutil
            for proc in psutil.process_iter(['name', 'cmdline']):
                if proc.info['name'] == 'python' and any('http_server.py' in arg for arg in proc.info['cmdline']):
                    os.kill(proc.pid, signal.SIGTERM)
                    logging.info(f"Server process (PID: {proc.pid}) stopped.")
                    return
            logging.info("No running http_server.py process found.")
        except ImportError:
            logging.error("psutil module not found. Unable to search for server process.")

    def _handle_process_not_found(self):
        logging.info("Server process not found. Lock file removed.")
        os.remove(self.lock_file)

    def _handle_invalid_lock_file(self, error):
        logging.error(f"Error reading lock file: {error}")
        os.remove(self.lock_file)
        logging.info("Invalid lock file removed.")

    def _log_server_start(self):
        message = f"Server started. Serving directory '{self.directory}' at port {self.port}"
        logging.info(message)

    def _log_port_in_use(self):
        message = f"Port {self.port} is already in use. Please choose a different port."
        logging.error(message)

    def _cleanup(self):
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)


def arugment_parser():
    web_root_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(
        description="Simple HTTP Server with custom features"
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=8000,
        help="Port to run the server on"
    )
    parser.add_argument(
        '-l',
        '--log_dir',
        type=str,
        default=os.path.join(web_root_dir, 'logs'),
        help="Log directory path"
    )
    parser.add_argument(
        '-w',
        '--web_dir',
        type=str,
        default=os.path.join(web_root_dir, 'webUI'),
        help="WebUI directory path"
    )
    parser.add_argument(
        '-s',
        '--stop',
        action='store_true',
        help="Stop the running server"
    )
    parser.add_argument(
        '-r',
        '--restart',
        action='store_true',
        help="Restart the server"
    )
    return parser.parse_args()


if __name__ == "__main__":
    # add argument parser
    args = arugment_parser()
    
    # init logger
    init_logger(args.log_dir)
    logging.info(str(args))
    
    # init server manager
    server = ServerManager(port=args.port, directory=args.web_dir)
    
    # handle stop, restart, run
    if args.stop:
        server.stop()
    elif args.restart:
        server.restart()
    else:
        server.run()