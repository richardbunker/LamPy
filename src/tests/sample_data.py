from pyweb_types import Headers, Request


class SampleData:
    def event(self, method: str, path: str) -> Request:
        headers: Headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Content-Length": "0",
            "Host": "localhost:8000",
            "User-Agent": "HTTPie/2.4.0",
        }
        request: Request = {
            "headers": headers,
            "requestContext": {
                "http": {
                    "path": path,
                    "method": method,
                }
            },
            "queryStringParameters": None,
            "body": None,
        }
        return request
