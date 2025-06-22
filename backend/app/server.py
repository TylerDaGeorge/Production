from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from .main import app

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, code=200, content_type='application/json'):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        handler = app.routes.get(('GET', self.path))
        if not handler:
            self._set_headers(404)
            self.wfile.write(b"{}")
            return
        result = handler()
        self._set_headers(200)
        self.wfile.write(json.dumps(result).encode())

    def do_POST(self):
        handler = app.routes.get(('POST', self.path))
        if not handler:
            self._set_headers(404)
            self.wfile.write(b"{}")
            return
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8') if length > 0 else '{}'
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {}
        result = handler(data)
        self._set_headers(200)
        self.wfile.write(json.dumps(result).encode())


def run(host="127.0.0.1", port=8000):
    server_address = (host, port)
    httpd = HTTPServer(server_address, Handler)
    print(f"Serving on http://{host}:{port} (Press CTRL+C to stop)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == "__main__":
    run()
