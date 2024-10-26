from api import Api


def lambda_handler(event, context):
    api = Api()
    response = api.handle(event)
    return response
