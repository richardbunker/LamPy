import re
from typing import Dict, List
from application_types import Handler, Headers, Request, Response, RouteMap
from logger import Logger


class PyWeb:
    """
    LamPy is a simple web framework for AWS Lambda.
    It is designed to be used with API Gateway.
    """

    def __init__(self) -> None:
        self.routes: RouteMap = {}

    def GET(self, path: str, handler: Handler) -> None:
        """
        Register a GET route.
        """
        if "GET" not in self.routes:
            self.routes["GET"] = {}

        self.routes["GET"].update({path: handler})

    def POST(self, path: str, handler: Handler) -> None:
        """
        Register a POST route.
        """
        if "POST" not in self.routes:
            self.routes["POST"] = {}

        self.routes["POST"].update({path: handler})

    def handle(self, awg_event: Request) -> Response:
        """
        Start the LamPy application.
        """
        # Log the request
        Logger.request(awg_event)

        # Get the method
        method = awg_event["requestContext"]["http"]["method"]
        path = awg_event["requestContext"]["http"]["path"]

        # Get the route
        method_routes = self.routes.get(method)

        # Check if the route exists
        if method_routes is None:
            return self.lampy_response(503, "Method not allowed", {})

        handler = self._match_route(method_routes, path)
        if handler is None:
            return self.lampy_response(404, "Not found", {})

        path_params = self._process_path_params(path, [route for route in method_routes])
        return handler(awg_event, path_params)

    def _process_path_params(self, path: str, method_routes: List[str]) -> Dict[str, str]:
        path_params: Dict[str, str] = {}
        for route in method_routes:
            if ":" in route:
                route_parts = route.split("/")
                path_parts = path.split("/")
                if len(route_parts) != len(path_parts):
                    continue
                for i, route_part in enumerate(route_parts):
                    if ":" in route_part:
                        path_params[route_part[1:]] = path_parts[i]
        return path_params

    def _match_route(self, routes, path) -> Handler | None:
        # Iterate over the route patterns
        for route in routes:
            # Replace route placeholders with regex patterns
            pattern = re.sub(r":\w+", r"(\\w+)", route)
            pattern = f"^{pattern}$"
            if re.match(pattern, path):
                return routes[route]
        return None

    def lampy_response(self, status_code: int, body: str, headers: Headers) -> Response:
        """
        Create a response object.
        """
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"
        response: Response = {
            "statusCode": status_code,
            "headers": headers,
            "body": body,
        }
        return response
