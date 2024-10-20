from http.server import BaseHTTPRequestHandler, HTTPServer
from app.lampy import LamPy

class LambdaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()

    def do_OPTIONS(self):
        self.handle_request()

    def _parse_query_string(self):
        query_params = {}
        if "?" in self.path:
            query_param_string = self.path.split("?")[1]
            params = query_param_string.split("&")
            for param in params:
                if "=" in param:
                    key, value = param.split("=")
                    query_params[key] = value
        return query_params

    def _parse_body(self):
        body = None
        if 'Content-Length' in self.headers:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            body = post_data.decode('utf-8')
            return body

    def _parse_headers(self):
        headers = {}
        for key, value in self.headers.items():
            headers[key] = value
        return headers

    def _request_adapter(self):
        path = self.path.split("?")[0]
        query_params = self._parse_query_string()
        body = self._parse_body()
        req = {
            "headers": self._parse_headers(),
            "http": {
                "path": path,
                "method": self.command,
            }
        }
        if query_params:
            req["queryStringParameters"] = query_params
        if body:
            req["body"] = body
        return req

    def handle_request(self):
        agw_event = self._request_adapter()
        app = LamPy()
        response = app.handle(agw_event)
        
        # Send a response back to the client
        self.send_response(response["statusCode"])
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(response["body"].encode("utf-8"))

def run(server_class=HTTPServer, handler_class=LambdaHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting HTTP server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
