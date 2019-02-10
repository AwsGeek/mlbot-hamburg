import os
import re
import json
import boto3
from botocore.vendored import requests

lam = boto3.client('lambda')

def classify_aircraft(url):

    aircraft = "None";    
    result = lam.invoke(
        FunctionName=os.environ['DetectorName'],
        InvocationType='RequestResponse',
        Payload=json.dumps({ "url": url })
    )
    detected = json.loads(result['Payload'].read().decode('utf8'))

    if len(detected) == 1 and detected[0]['score'] > 99:
        result = lam.invoke(
            FunctionName=os.environ['ClassifierName'],
            InvocationType='RequestResponse',
            Payload=json.dumps({ "url": url})
        )
        aircraft = json.loads(result['Payload'].read().decode('utf8'))
        
    return aircraft

def lambda_handler(event, context):
    print(event)
    
    for record in event['Records']:

        request = json.loads(record['body'])
        
        event = request['event']
        text = event['text']
        
        matches = re.search( 'classify\s+<(.*)>', text, re.IGNORECASE)
        if matches:
            
            url = matches.group(1)
            aircraft = classify_aircraft(url)
            print(aircraft)

            data = {'token':os.environ['SlackToken'], 
                    'channel':event['channel'],
                    'thread_ts':event['ts'],
                    'text': "Aircraft detected: " + aircraft } 
              
            r = requests.post(url = 'https://slack.com/api/chat.postMessage', data = data)     



