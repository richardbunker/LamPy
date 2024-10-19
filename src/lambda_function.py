from app.lampy import LamPy
import json

def lambda_handler(event, context):
    print("Event: ", json.dumps(event))
    app = LamPy()
    response = app.handle(event)
    return response
