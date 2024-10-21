import time
from application_types import Request

class Logger:
    """
        Logger is a simple class to log events to stdout.
    """
    @staticmethod
    def request(req: Request) -> None:
        """
            Log the request to stdout.
        """
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        output = f"\n📬 {current_time} [{req['requestContext']['http']['method']}] {req['requestContext']['http']['path']}"
        if 'queryStringParameters' in req:
            output += f" | Query Params: {req['queryStringParameters']}"
        if 'headers' in req:
            output += f" | Headers: {req['headers']}"
        if 'body' in req:
            output += f" | Body: {req['body']}"
        output += "\n"
        print(output)

