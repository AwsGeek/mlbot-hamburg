import os
import json
import boto3

session = boto3.session.Session()
sqs = session.client('sqs')

def response(code, body):
    return {
        'statusCode': str(code),
        'body': body,
        'headers': { 'Content-Type': 'application/json'}
    }
 
def success(res=None):
    return response(200, json.dumps(res))
 
def failure(err):
    return response(400, err.message)
 
def lambda_handler(event, context):
 
    print(event)
    
    params = json.loads(event['body'])
    if params['type'] == "url_verification":
        return success(  {'challenge': params['challenge']} )

    if params['type'] == "event_callback":

        response = sqs.send_message(
            QueueUrl=os.environ['QueueUrl'],
            MessageBody=(event['body'])
        )
        return success()        
        
    return failure(Exception('Invalid event type: %s' % (params['type'])))
