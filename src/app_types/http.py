from typing import TypedDict, Optional

class Headers(TypedDict, total=False):
    pass

class HTTP(TypedDict):
    path: str
    method: str

class QueryStringParameters(TypedDict, total=False):
    pass

class Request(TypedDict):
    headers: Optional[Headers]
    http: HTTP
    queryStringParameters: Optional[QueryStringParameters]
    body: Optional[str]


class Response(TypedDict):
    statusCode: int
    body: str
    headers: Optional[Headers]
