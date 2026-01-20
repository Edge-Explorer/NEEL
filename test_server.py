from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"✅ Received GET request from {self.client_address}")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = json.dumps({"status": "ok", "message": "Connection successful!"})
        self.wfile.write(response.encode())
    
    def do_POST(self):
        print(f"✅ Received POST request from {self.client_address}")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = json.dumps({"status": "ok", "message": "POST received!"})
        self.wfile.write(response.encode())
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 9000), SimpleHandler)
    print("🚀 Test server running on http://0.0.0.0:9000")
    print("📱 Try accessing http://192.168.1.106:9000 from your phone's browser")
    print("   If you can't access it, your router has AP Isolation enabled")
    server.serve_forever()
