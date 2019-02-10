import os
import json
import boto3

from botocore.vendored import requests
 
sage = boto3.Session().client(service_name='runtime.sagemaker') 
names = ['Airbus A320','Boeing 747','Dornier 328']

def lambda_handler(event, context):
    print(event)  
 
    url = event["url"]

    bytes = requests.get(url).content
    
    response = sage.invoke_endpoint(EndpointName=os.environ['EndpointName'], 
                                    ContentType='application/x-image', 
                                    Body=bytes)
    scores = response['Body'].read()
    scores = json.loads(scores)

    score = max(scores)
    aircraft = names[scores.index(score)]

    result =  "%s (%.1f)" % (aircraft, 100*score)
    print(result)
    
    return result
