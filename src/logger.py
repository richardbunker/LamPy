import time
from pyweb_types import Environment, Request


class Logger:
    """
    Logger is a simple class to log events to stdout.
    """

    @staticmethod
    def request(req: Request, environment: Environment) -> None:
        """
        Log the request to stdout.
        """
        if environment != "LOCAL":
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            method = req["requestContext"]["http"]["method"]
            path = req["requestContext"]["http"]["path"]
            output = f"\n📬 {current_time} [{method}] {path}"
            if "queryStringParameters" in req:
                query_params = req["queryStringParameters"]
                output += f" | Query Params: {query_params}"
            if "headers" in req:
                headers = req["headers"]
                output += f" | Headers: {headers}"
            if "body" in req:
                body = req["body"]
                output += f" | Body: {body}"
            output += "\n"
            print(output)
