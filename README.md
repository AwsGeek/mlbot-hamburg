# Build a Serverless Machine Learning Bot
<p align="center"><img src="images/boeing-747.jpg"></p>

## Overview
In this tutorial, you will build a serverless bot using Slack and Amazon Web Services, including AWS Lambda, Amazon SageMaker, and API Gateway. The bot will help you identify aircraft founbd in images. 
### Objectives
In this tutorial you will perform the following tasks:

* **[Lab 1: Train an aircraft classifier](lab1)** -
In this lab you will use Amazon SageMaker to train an aircraft classification model and then create an AWS Lambda function to act as a private interface for your Amazon SageMaker endpoint.
* **[Lab 2: Build an aircraft detector](lab2)** -
In this lab you will use Amazon Rekognition to detect aircraft and create and AWS Lambda function to interact with Rekognition.
* **[Lab 3: Create a private interface](lab3)** -
In this lab you will use AWS Lambda to create a private interface for your Amazon SageMaker endpoint
* **[Lab 3: Build a public interface](lab3)** -
In this lab you will use Amazon API Gateway and AWS Lambda to create a public interface for your aircraft classifier
* **[Lab 4: Build a Slack bot](lab4)** -
In this lab you will create a Slack bot that allows you to send request to your aircraft classify
* **[Lab 5: Cleanup](lab5)** - 
In this lab you will tear down all AWS resources created during this tutorial.

### Prerequisites
* AWS account
* Slack account

_**Note:** For this tutorial you will be creating and using AWS resources including Amazon S3, SageMaker, Lambda, and API Gateway. All AWS resources must be created in the same AWS region._

_Amazon SageMaker is currently available in the following regions: US East (Ohio), US East (N. Virginia), US West (Oregon), Asia Pacific (Seoul), Asia Pacific (Sydney), Asia Pacific (Tokyo), EU (Frankfurt), EU (Ireland), and AWS GovCloud (US)._

_For an up-to-date list of services and supported regions, see https://docs.aws.amazon.com/general/latest/gr/rande.html_

# Lab 1: Train an aircraft classifier
In this lab you will use Amazon SageMaker and Amazon Lambda to help classify single aircraft in an image.

## Task 1: Create an S3 bucket
The S3 bucket will be used to store training images for the SageMaker model and artifacts, as well as other temporary resources
1. Browse to the Amazon S3 console to create a new bucket: https://console.aws.amazon.com/s3/home#/create
2. Click on the **Create Bucket** button and enter the following information
* Bucket name: a unique, DNS compliant bucket name.
* Region: The same region as your other AWS resources in this workshop
3. Click on the **Create** button to finish.

## Task 2: Create a SageMaker Notebook
1. Browse to the Amazon SageMaker console to create a new notebook: https://console.aws.amazon.com/sagemaker/home#/notebook-instances/create
2. Enter the following information for your notebook:
* Notebook instance name: **mlbot**
* Notebook instance type: **ml.t2.medium**
* IAM role: **Create a new role**
* VPC: **No VPC**
* Lifecycle configuration: **No configuration**
* Encryption key: **No Custom Encryption**
* Volume Size in GB: **5**
3. When prompted to create an IAM role, enter the name of the S3 bucket create in the previous task, then click the **Create role** button to continue.
4. Click on the **Create notebook instance** button to finish
5. Wait for your notebook status to change to **InService**, then click the **Open** link. This will open Jupyter notebook in another tab.
6. Load the Jupyter notebook for this lab by clicking the **Upload** button and providing the file to use: https://www.awsgeek.com/mlbot/mlbot.ipynb
7. Click in the uploaded notebook name to open the notebook

## Task 3. Train the SageMaker model
Execute the following steps in order to train your model
1. Prepare for training. In cell 1, replace ```<replace with your bucket name>``` with the bucket name you created in a previous task, then click on the **Run** button to run this cell of the notebook.
2. Train the model. Select this cell, then click on the **Run** button to train the model. Training this model takes approximatley 5 to 10 minutes using a single ml.p3.2xlarge training instance. 
3. While waiting for the training job to finish, browse to the SageMaker console and find training job. Click on the training job and open to view details and log activity.
4. Deploy the model. Select this cell, then click on the **Run** button to deploy the model. Deploying this model can take several minutes. Note the endpoint name and ARN for later use.
5. Finally, Test the model. Select this cell, then click on the **Run** button to test the model. Verify the classification matches the displayed aircraft.

## Task 4: Create a Lambda function
Create an AWS Lambda function that uses Amazon SageMaker to classify an aircraft in an image
1. Browse to the AWS Lambda console to create a new function: https://console.aws.amazon.com/lambda/home#/create
2. Select the **Author from Scratch** option:
3. Fill out the following information for the Lambda function:
* Name: **mlbot-classify**
* Runtime: **Python 3.6**
* Role: **Create a custom role**
4. Specify the following information for the IAM role, then click the **Allow** button to continue:
* IAM Role: **Create a new IAM Role**
* Role Name: **mlbot-classify**
5. Click the **Create** function' button to finish:

## Task 2: Update the IAM role
Update the IAM role to allow invocation of the SageMaker InvokeEndpoint API
1. Browse to the AWS IAM console to edit the **mlbot-classify** IAM role: https://console.aws.amazon.com/iam/home#/roles/mlbot-classify
2. Click on the **Add inline policy** button
3. Click on the **JSON** tab and replace the existing policy with the following. Replace ```<S3 bucket name>``` with the name of your S3 bucket.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "mlbot-classify",
            "Effect": "Allow",
            "Action": "sagemaker:InvokeEndpoint",
            "Resource": "<SageMaker Endpoint ARN>"
        }
    ]
}
```
4. Click on the **Review policy** button to continue
5. Name the policy **mlbot-classify**, then click on the **Create policy** button to finish

## Task 3: Update the Lambda function
Update the Lambda Function invoke the Amazon SageMaker InvokeEndpoint API
1. Browse to the AWS Lambda console to edit the **mlbot-classify** Lambda function: https://console.aws.amazon.com/lambda/home#/functions/mlbot-classify
2. Replace the existing Lambda function code with the following. Replace ```<SageMaker endpoint name>``` with the name of your SageMaker endpoint. 
```
import json
import boto3

from botocore.vendored import requests
 
sage = boto3.Session().client(service_name='runtime.sagemaker') 
names = ['airbus-a320','boeing-747','dornier-328']

def lambda_handler(event, context):
   
    url = event["url"]

    # download image bytes
    bytes = requests.get(url).content
    
    # classify aircraft in the image
    response = sage.invoke_endpoint(EndpointName='<SageMaker endpoint name>', 
                                   ContentType='application/x-image', 
                                   Body=bytes)
    scores = response['Body'].read()
    scores = json.loads(scores)

    aircraft = ""
    if max(scores) > 0.90:
        aircraft = names[scores.index(max(scores))]
    
    return aircraft
```
3. Click the **Save** button to finish

## Task 4: Test the Lambda function
Create a test event and test your Lambda function 
1. Browse to the AWS Lambda console to edit the **mlbot-classify** Lambda function: https://console.aws.amazon.com/lambda/home#/functions/mlbot-classify
2. Click on the **Select a test event..** drop down and select **Configure test events**
3. Specify the following onformation for the test event:
* Event template: **Hello World**
* Event name: **mlbot-classify**
* Code:
```
{
  "url": "https://www.awsgeek.com/mlbot/airbus-a320.jpg"
}
```
4. Click on the **Create** button to continue
5. Click click on the **Test** button to verify operation of your Lambda function and invocation of your SageMaker endpoint.

## This is the end of the lab
