from typing import Callable, Dict, NotRequired, TypedDict, Optional

Headers = TypedDict("Headers", {"Content-Type": str}, total=False)


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
    headers: NotRequired[Headers]


PathParams = Dict[str, str]
Handler = Callable[[Request, Optional[PathParams]], Response]
Routes = Dict[str, Handler]


class RouteMap(TypedDict, total=False):
    GET: Routes
    POST: Routes
