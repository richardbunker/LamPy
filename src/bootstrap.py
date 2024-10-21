from typing import Callable
from application_types import Request, Response
from application import LamPy
import json

def index(request: Request) -> Response:
    body = json.dumps(request)
    return {
        'statusCode': 200,
        'body': body,
    }

def bootstrap(event: Request) -> Response:
    app = LamPy()
    app.GET('/', index)
    response = app.handle(event)
    return response

