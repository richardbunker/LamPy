from typing import TypedDict, Optional

class Headers(TypedDict, total=False):
    pass

class HTTP(TypedDict):
    path: str
    method: str

class RequestContext(TypedDict):
    http: HTTP

class QueryStringParameters(TypedDict, total=False):
    pass

class Request(TypedDict):
    headers: Optional[Headers]
    requestContext: RequestContext
    queryStringParameters: Optional[QueryStringParameters]
    body: Optional[str]


class Response(TypedDict):
    statusCode: int
    body: str
    headers: Optional[Headers]
