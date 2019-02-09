# Lab 5: Build a Slack bot
In this lab you will create a Slack bot that allows you to send requests to your object detector

## Task 1: Create a Slack app
1. Navigate to https://api.slack.com/apps?new_app=1, login to your workspace if necessary.
2. Create a new Slack app named **mlbot**, select your workspace, then click the **Create App** button to continue
3. In the **Features** section, select **Bot Users**, then click the **Add Bot User** button. 
4. Specify the following information for your bot user, then click the **Add Bot User** button to continue:
* Display name: **mlbot**
* Default username: **mlbot**
* Always Show My Bot as Online: **On**
5. In the **Settings** section, select **Install App**, then click the **Install App to Workspace** button. Follow the instructions to authorize the installation and use of your new app. 

## Task 2: Create an event subscription  
1. In the **Features** section, select **Event Subscriptions**, then click the **Enable Events** switch. 
2. For the **Request URL**, specify the API Gateway endpoint URL you captured in the previous lab. 
The Request URL will show **Verified** if Slack can successfully reach your mlbot Lambda function via the API Gateway
3. In the **Subscribe to Bot Events** section, click on the **Add Bot User Event** button, then select the **app_mentions** event type. Click in the **Save Changes** button to finish.

## Task 3: Update the dispatch Lambda functions
Update code to the **mlbot-dispatch** funtion to parse and dispatch incomoing requests from your Slack bot. 
1. Browse to the AWS Lambda console to edit the **mlbot-dispatch** Lambda function: https://console.aws.amazon.com/lambda/home#/functions/mlbot-dispatch
2. Replace the **lambda_function.py** template code with the following. In addition, replace **```<SQS queue URL>```** with the URL of your SQS queue
```
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
            QueueUrl="<SQS queue URL>",
            MessageBody=(event['body'])
        )
        return success()        
        
    return failure(Exception('Invalid event type: %s' % (params['type'])))
```
3. Click the **Save** button to finish

## Task 4: Update the handler Lambda functions
Update code to the **mlbot-handler** funtion to parse and dispatch incomoing requests from your Slack bot. 
1. Browse to the AWS Lambda console to edit the **mlbot-handler** Lambda function: https://console.aws.amazon.com/lambda/home#/functions/mlbot-handler
2. Replace the **lambda_function.py** template code with the following. In addition, replace **```<Bot User OAuth Access Token>```** with the token captured earlier in this lab
```
import re
import json
import boto3
from botocore.vendored import requests

lam = boto3.client('lambda')

def classify_aircraft(url):

    aircraft = "None";    
    result = lam.invoke(
        FunctionName="mlbot-detect",
        InvocationType='RequestResponse',
        Payload=json.dumps({ "url": url })
    )
    detected = json.loads(result['Payload'].read().decode('utf8'))

    if len(detected) == 1 and detected[0]['score'] > 99:
        result = lam.invoke(
            FunctionName="mlbot-classify",
            InvocationType='RequestResponse',
            Payload=json.dumps({ "url": url})
        )
        aircraft = json.loads(result['Payload'].read().decode('utf8'))
        
    return aircraft

def lambda_handler(event, context):
    
    for record in event['Records']:

        request = json.loads(record['body'])
        
        event = request['event']
        text = event['text']
        
        matches = re.search( 'classify\s+<(.*)>', text, re.IGNORECASE)
        if matches:
            
            url = matches.group(1)
            aircraft = classify_aircraft(url)
            

            data = {'token':'<Bot User OAuth Access Token>', 
                    'channel':event['channel'],
                    'thread_ts':event['ts'],
                    'text': aircraft } 
              
            r = requests.post(url = 'https://slack.com/api/chat.postMessage', data = data)     
```
3. Click the **Save** button to finish

## Task 4: Test the Slack bot
1. Send the following request to the Slack bot and verify the response from the Lambda function
```
@mlbot classify https://www.awsgeek.com/hamburg19/airbus-a320.jpg
@mlbot classify https://www.awsgeek.com/hamburg19/boeing-747.jpg
@mlbot classify https://www.awsgeek.com/hamburg19/dornier-328.jpg
```

2. Experiment with other images to verify that the bot operates corretly on images with and without aircraft in them.

## This is the end of the lab
