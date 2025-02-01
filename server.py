from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()
    
    def do_GET(self):
        print(f"Requested path: {self.path}")
        print(f"Current directory: {os.getcwd()}")
        try:
            super().do_GET()
            print(f"Successfully served: {self.path}")
        except Exception as e:
            print(f"Error serving {self.path}: {str(e)}")
            self.send_error(404, f"File not found: {self.path}")

def run_server(port=8000):
    handler = CORSRequestHandler
    handler.extensions_map.update({
        '.js': 'application/javascript',
        '.css': 'text/css',
    })
    
    with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
        print(f"Server running at http://0.0.0.0:{port}")
        print(f"Serving files from: {os.getcwd()}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()

if __name__ == "__main__":
    run_server()