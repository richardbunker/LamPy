from typing import Callable, Dict, TypedDict, Optional

Headers = TypedDict('Headers', {'Content-Type': str}, total=False)

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


class Response(TypedDict, total=False):
    statusCode: int
    body: str
    headers: Optional[Headers]

Handler = Callable[[Request], Response]

Route = Dict[str, Handler]
    
class RouteMap(TypedDict, total=False):
    GET: Optional[Route]
    POST: Optional[Route]
