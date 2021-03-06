# Build an aircraft detector
In this lab you will use AWS Lambda and Amazon Rekognition to create an aircraft detector

## Task 1: Create a Lambda function
Create an AWS Lambda function that uses Amazon SageMaker to classify an aircraft in an image
1. Browse to the AWS Lambda console to create a new function: https://console.aws.amazon.com/lambda/home#/create
2. Select the **Author from Scratch** option:
3. Fill out the following information for the Lambda function:
* Name: **mlbot-detect**
* Runtime: **Python 3.7**
* Permissions: **Expand: Choose or create an execution role**
4. Specify the following information for Execution role:
* Select **Create a new role with basic Lambda permissions**
* A Role Name will be created containing: **mlbot-detect** name as prefix, the role name looks like mlbot-detect-role-kjerkt
5. Click the **Create** function' button to finish:
Update the Lambda Function classify an aircraft in an image using Amazon SageMaker InvokeEndpoint API
6. Edit the Lambda function, replace with the following Python code. 
```
import boto3
from botocore.vendored import requests

rek = boto3.client('rekognition', region_name='eu-west-1')

def lambda_handler(event, context):
    print(event)
    
    url = event['url']
    bytes = requests.get(url).content
    image = {'Bytes': bytes }
    
    results = []
    try:
        
      response = rek.detect_labels( Image = image )

      for label in response['Labels']:
        if label['Name'] == 'Airplane':
          for instance in label['Instances']:

            results.append( { 
                'label' : label['Name'],
                'score' : instance['Confidence'],
                'left'  : instance['BoundingBox']['Left'],
                'top'  : instance['BoundingBox']['Top'],
                'width'  : instance['BoundingBox']['Width'],
                'height'  : instance['BoundingBox']['Height']
            })

    except Exception as e:
      print(e)

    print(results)
    return results
```
7. Click the **Save** button to finish

## Task 2: Update the IAM role
Update the IAM role to allow invocation of the SageMaker InvokeEndpoint API
1. In **mlbot-detect** Lambda function scroll down to **Execution role** pane and click on **View the mlbot-detect-role-<id> role** to go the IAM role page.
2. Click on the **Add inline policy** button
3. Click on the **JSON** tab and replace the existing policy with the following.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "mlbot",
            "Effect": "Allow",
            "Action": "rekognition:DetectLabels",
            "Resource": "*"
        }
    ]
}
```
4. Click on the **Review policy** button to continue
5. Name the policy **mlbot-detect**, then click on the **Create policy** button to finish

## Task 4: Test the Lambda function
Create a test event and test your Lambda function 
1. Browse to the AWS Lambda console to edit the **mlbot-detect** Lamda function: https://console.aws.amazon.com/lambda/home#/functions/mlbot-detect
2. Click on the **Select a test event..** drop down and select **Configure test events**
3. Specify the following onformation for the test event:
* Event template: **Hello World**
* Event name: **mlbotdetect**
* Code:
```
{
  "url": "https://github.com/AwsGeek/mlbot-hamburg/raw/master/lab5/airbus-a320.jpg"
}
```
4. Click on the **Create** button to continue
5. Click click on the **Test** button, then verify the output of the test matches the example output below

## This is the end of the lab
