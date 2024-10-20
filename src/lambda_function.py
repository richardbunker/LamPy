from app.lampy import LamPy

def lambda_handler(event, context):
    app = LamPy()
    response = app.handle(event)
    return response
