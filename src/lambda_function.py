from bootstrap import bootstrap

def lambda_handler(event, context):
    return bootstrap(event)
