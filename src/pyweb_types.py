from typing import Callable, Dict, TypedDict, Optional

Headers = Dict[str, str]
QueryStringParameters = Dict[str, str]


class HTTP(TypedDict):
    path: str
    method: str


class RequestContext(TypedDict):
    http: HTTP


class Request(TypedDict):
    headers: Headers
    requestContext: RequestContext
    queryStringParameters: Optional[QueryStringParameters]
    body: Optional[str]


class Response(TypedDict):
    statusCode: int
    body: str
    headers: Headers


PathParams = Dict[str, str]
Handler = Callable[[Request, PathParams], Response]
Routes = Dict[str, Handler]


class RouteMap(TypedDict, total=False):
    GET: Routes
    POST: Routes
