# Request handler
In this lab you will use an SQS queue and Lambda function to handle incoming requests.

## Task 1: Create a Lambda function
Create an AWS Lambda function that coordinates detection and classification of aircraft in images.
1. Browse to the AWS Lambda console to create a new function: https://console.aws.amazon.com/lambda/home#/create
2. Select the **Author from Scratch** option:
3. Fill out the following information for the Lambda function:
* Name: **mlbot-handler**
* Runtime: **Python 3.7**
* Permissions: **Expand: Choose or create an execution role**
4. Specify the following information for Execution role:
* Select **Create a new role with basic Lambda permissions**
* A Role Name will be created containing: **mlbot-handler** name as prefix, the role name looks like mlbot-handler-role-kjer4h
5. Click the **Create** function' button to finish:
6. Edit the Lambda function, replace with the following Python code. 
```
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
    
    print("Aircraft detected: " + classify_aircraft(event['url']))
```
7. Create environment variables **DetectorName** and **ClassifierName** and set to the names of your Lambda functions **mlbot-detect** and **mlbot-classify**
8. Click the **Save** button to finish

## Task 2: Update the IAM role
Update the IAM role to allow invocation of the **mlbot-detect** and **mlbot-classify** Lambda functions
1. In **mlbot-handler** Lambda function scroll down to **Execution role** pane and click on **View the mlbot-handler-role-<id> role** to go the IAM role page.
2. Click on the **Add inline policy** button
3. Click on the **JSON** tab and replace the existing policy with the following. Include the ARNs of your **mlbot-detect** and **mlbot-classify** Lambda functions:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid" : "mlbot",
            "Effect": "Allow",
            "Action": "lambda:InvokeFunction",
            "Resource": [
                "<mlbot-detect Function ARN>",
                "<mlbot-classify Function ARN>"
            ]
        }
    ]
}
```
4. Click on the **Review policy** button to continue
5. Name the policy **mlbot-handler**, then click on the **Create policy** button to finish

## Task 3: Test the Lambda function
Create a test event and test your Lambda function 
1. Browse to the AWS Lambda console to edit the **mlbot-handler** Lamda function: https://console.aws.amazon.com/lambda/home#/functions/mlbot-handler
2. Click on the **Select a test event..** drop down and select **Configure test events**
3. Specify the following onformation for the test event:
* Event template: **Hello World**
* Event name: **mlbot**
* Code:
```
{
  "url": "https://github.com/AwsGeek/mlbot-hamburg/raw/master/lab5/airbus-a320.jpg"
}
```
4. Click on the **Create** button to continue
5. Click click on the **Test** button to verify operation of your Lambda function


## Task 4: Create an SQS Queue
1. Browse to the SQS console to create an SQS queue for requests: https://console.aws.amazon.com/sqs/home#create-queue
2. Fill out the following information for the queue:
* Name: **mlbot-requests**
* Region: same as other resources
* Type: **Standard Queue**
3. Click on the **Quick Create Queue** button to use other detfault settings and create the queue

4. Once created, select the **mlbot-requests** queue, and from the **Queue Actions** dropdown, select **Configure Trigger for Lambda Function**
5. Choose your **mlbot-handler** Lambda function, then click the **Save** button.

What happens?

## Task 5: Update the IAM role (again)
Update the IAM role to allow the Lambda function to interact with the SQS queue
1. In **mlbot-handler** Lambda function scroll down to **Execution role** pane and click on **View the mlbot-handler-role-<id> role** to go the IAM role page.
2. Click on the **Add inline policy** button
3. Click on the **JSON** tab and replace the existing policy with the following. Include the ARN of your **SQS queue**:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "mlbot",
            "Effect": "Allow",
            "Action": [
                "sqs:DeleteMessage",
                "sqs:ReceiveMessage",
                "sqs:GetQueueAttributes"
            ],
            "Resource": "<SQS queue ARN>"
        }
    ]
}
```
4. Click on the **Review policy** button to continue
5. Name the policy **mlbot-handler-sqs**, then click on the **Create policy** button to finish

## Task 6: Create an SQS Trigger
1. Browse to the SQS console and select the **mlbot-requests** queue: https://console.aws.amazon.com/sqs/home
2. From the **Queue Actions** dropdown, select **Configure Trigger for Lambda Function**
3. Choose your **mlbot-handler** Lambda function, then click the **Save** button.

## Task 7: Update the Lambda function
1. Browse to the AWS Lambda console to edit the **mlbot-handler** Lambda function: https://console.aws.amazon.com/lambda/home#/functions/mlbot-handler
2. Replace just the lambda_handler code in your function with the following code snippet. This will take requests off the queue one at a time and process.:
```
...

def lambda_handler(event, context):
    print(event)
    
    for record in event['Records']:

        request = json.loads(record['body'])
        
        print("Aircraft detected: " + classify_aircraft(request['url']))
```
3. Click the **Save** button to finish

## Task 8: Test the Lambda function
Test the Lambda function and SQS trigger
1. Browse to the SQS console and select the **mlbot-requests** queue: https://console.aws.amazon.com/sqs/home
2. From the **Queue Actions** dropdown, select **Send a Message**
3. Use the following to as the body of the message:
```
{
  "url": "https://github.com/AwsGeek/mlbot-hamburg/raw/master/lab5/airbus-a320.jpg"
}
```
4. Click on the **Send Message** button to continue
5. Verify the trigger was succesfull by inspecting the **mlbot-handler** function logs

