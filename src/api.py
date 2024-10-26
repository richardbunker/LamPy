from application_types import PathParams, Request, Response
from application import PyWeb
import json
import boto3


class Api:
    def __init__(self) -> None:
        self.app = PyWeb()
        self.app.GET("/", self.index)
        self.app.GET("/users/:user_id", self.show_user)

    # Define the route handlers
    def index(self, request: Request, path_params: PathParams) -> Response:
        print("Botocore version:", boto3.__version__)
        print(path_params, request)
        body = json.dumps({"request": request, "message": "Hello, World!"})
        return self.app.response(200, body)

    def show_user(self, request: Request, path_params: PathParams) -> Response:
        print(path_params, request)
        user_id = path_params.get("user_id")
        body = json.dumps({"user_id": user_id})
        return self.app.response(200, body)

    # Define a method to handle the request
    def handle(self, event: Request) -> Response:
        response = self.app.handle(event)
        return response
