import http.server
import socketserver
import json
import os

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/file_list':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            file_list = [f for f in os.listdir('data') if f.endswith('.md')]
            self.wfile.write(json.dumps(file_list).encode())
        else:
            super().do_GET()

if __name__ == "__main__":
    PORT = 8001
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
