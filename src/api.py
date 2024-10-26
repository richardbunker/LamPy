from application_types import PathParams, Request, Response
from application import PyWeb
import json


class Api:
    def __init__(self) -> None:
        self.app = PyWeb()
        self.app.GET("/", self._index)
        self.app.GET("/users/:user_id", self._show_user)

    def handle(self, event: Request) -> Response:
        response = self.app.handle(event)
        return response

    def _index(self, request: Request, path_params: PathParams | None) -> Response:
        body = json.dumps({"request": request, "message": "Hello, World!"})
        return self.app.lampy_response(200, body, {})

    def _show_user(self, request: Request, path_params: PathParams | None) -> Response:
        body = json.dumps({"request": request, "user_id": path_params.get("user_id") if path_params else None})
        return self.app.lampy_response(200, body, {})
