import re
from typing import Dict, Tuple
from pyweb_types import Environment, Handler, Headers, Request, Response, RouteMap, Routes
from logger import Logger


class PyWeb:
    """
    PyWeb is a simple and light-weight RESTful framework.
    Copyright (c) 2024 Richard Bunker
    """

    def __init__(self, environment: Environment) -> None:
        self.environment: Environment = environment
        self.routes: RouteMap = {}

    def GET(self, path: str, handler: Handler) -> None:
        """
        Register a GET route.
        """
        if "GET" not in self.routes:
            routes: Routes = {}
            self.routes["GET"] = routes

        self.routes["GET"].update({path: handler})

    def POST(self, path: str, handler: Handler) -> None:
        """
        Register a POST route.
        """
        if "POST" not in self.routes:
            routes: Routes = {}
            self.routes["POST"] = routes

        self.routes["POST"].update({path: handler})

    def handle(self, req: Request) -> Response:
        """
        Start the PyWeb pyweb.
        """
        # Log the request
        Logger.request(req, self.environment)

        # Get the method
        method = req["requestContext"]["http"]["method"]
        path = req["requestContext"]["http"]["path"]

        # Check if the method is supported
        if method not in self.routes:
            return self.response(405, "Method not allowed", {})
        else:
            # Get a method's routes
            routes: Routes = self.routes[method]

            # Check if the route exists
            matched = self._match_route(routes, path)
            if matched is None:
                return self.response(404, "Not found", {})

            # Get the route and handler
            route, handler = matched

            # Call the handler
            return handler(req, self._init_path_params(route, path))

    def _init_path_params(self, route: str, path: str) -> Dict[str, str]:
        """
        Initialise path parameters from the path.
        route: '/user/:id'
        path: '/user/123'

        returns: {'id': '123'}
        """
        path_params: Dict[str, str] = {}
        if ":" not in route:
            return path_params

        route_parts = route.split("/")
        path_parts = path.split("/")
        for i, route_part in enumerate(route_parts):
            if ":" in route_part:
                path_params[route_part[1:]] = path_parts[i]
        return path_params

    def _match_route(self, routes: Routes, path: str) -> Tuple[str, Handler] | None:
        """
        Match the path to a route.
        """
        # Iterate over the route patterns
        for route in routes:
            # Replace route placeholders with regex patterns
            pattern = re.sub(r":\w+", r"(\\w+)", route)
            pattern = f"^{pattern}$"
            if re.match(pattern, path):
                handler: Handler = routes[route]
                return (route, handler)
        return None

    def response(self, status_code: int, body: str, headers: Headers = {}) -> Response:
        """
        Create an pyweb response object.
        """
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"
        response: Response = {
            "statusCode": status_code,
            "headers": headers,
            "body": body,
        }
        return response
