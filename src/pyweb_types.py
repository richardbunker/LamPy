from typing import Callable, Dict, Literal, TypedDict, Optional

Headers = Dict[str, str]
QueryStringParameters = Dict[str, str]
Method = Literal["GET", "POST", "PUT", "DELETE", "OPTIONS"]


class HTTP(TypedDict):
    path: str
    method: Method


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

RouteMap = Dict[Method, Routes]
