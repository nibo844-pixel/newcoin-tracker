from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("newcoin-tracker ok".encode())
    def log_message(self, *a):
        pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    HTTPServer(("0.0.0.0", port), H).serve_forever()
