import json
import re
from typing import Callable, cast
from application_types import Handler, Headers, Request, Response, Route, RouteMap
from logger import Logger

class LamPy:
    """
        LamPy is a simple web framework for AWS Lambda.
        It is designed to be used with API Gateway.
    """
    def __init__(self) -> None:
        self.routes: RouteMap = {}

    def GET(self, path: str, handler: Callable[[Request], Response]) -> None:
        """
            Register a GET route.
        """
        self.routes['GET'] = {
            path: handler,
        }

    def POST(self, path: str, handler: Callable[[Request], Response]) -> None:
        """
            Register a POST route.
        """
        self.routes['POST'] = {
            path: handler,
        }
        
    def handle(self, awg_event: Request) -> Response:
        """
            Start the LamPy application.
        """
        # Log the request
        Logger.request(awg_event)

        # Get the method
        method = awg_event['requestContext']['http']['method']
        path = awg_event['requestContext']['http']['path']

        # Get the route
        routes = self.routes.get(method)

        # Check if the route exists
        if routes is None:
            return self._create_response(503, 'Method not allowed', {})

        handler = self._match_route(routes, path)  
        if handler is None:
            return self._create_response(404, "Not found", {})
        return handler(awg_event)

    def _match_route(self, routes, path) -> Handler | None:
        # Iterate over the route patterns
        for route in routes:
            # Replace route placeholders with regex patterns
            pattern = re.sub(r":\w+", r"(\\w+)", route)
            pattern = f"^{pattern}$"
            if re.match(pattern, path):
                return routes[route]
        return None 

    def _create_response(self, status_code: int, body: str, headers: Headers) -> Response:
        """
            Create a response object.
        """
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"
        response: Response = {
            'statusCode': status_code,
            'headers': headers,
            'body': body,
        }
        return response
