import json


class LamPy:
    """
        LamPy is a simple web framework for AWS Lambda.
        It is designed to be used with API Gateway.
    """
    def handle(self, event):
        """
            Start the LamPy application.
        """
        print("Event: ", event)
        return {
          "statusCode": 200,
          "body": json.dumps(event),
          "headers": {
            "content-type": "application/json"
          }
        }
        
