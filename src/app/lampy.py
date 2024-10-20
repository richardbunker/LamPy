import json
from typing import cast
from app_types.http import Headers, Request, Response
from logger import Logger

class LamPy:
    """
        LamPy is a simple web framework for AWS Lambda.
        It is designed to be used with API Gateway.
    """
    def handle(self, awg_event: Request) -> Response:
        """
            Start the LamPy application.
        """
        # Log the request
        Logger.request(awg_event)

        response: Response = {
            "statusCode": 200,
            "body": json.dumps(awg_event),
            'headers': cast(Headers, {
                'Content-Type': 'application/json'
            })
        }
        return response
