
# Aircraft classifier
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
6. Load the Jupyter notebook for this lab by clicking the **Upload** button and providing the file to use: https://raw.githubusercontent.com/AwsGeek/mlbot-hamburg/master/lab1/mlbot.ipynb
7. Click in the uploaded notebook name to open the notebook

## Task 3. Train the SageMaker model
Execute the following steps in order to train your model
1. Prepare for training. In cell 1, replace **```<replace with your bucket name>```** with the bucket name you created in a previous task, then click on the **Run** button to run this cell of the notebook.
2. Train the model. Select this cell, then click on the **Run** button to train the model. Training this model takes approximately 10 minutes using a single ml.p3.2xlarge training instance. 
3. While waiting for the training job to finish, browse to the SageMaker console and find training job. Click on the training job and open to view details and log activity.
4. Deploy the model. Select this cell, then click on the **Run** button to deploy the model. Deploying this model can take several minutes. Note the endpoint name and ARN for later use.
5. Finally, Test the model. Select this cell, then click on the **Run** button to test the model. Verify the classification matches the displayed aircraft.

## Task 4: Create a Lambda function
Create an AWS Lambda function that uses Amazon SageMaker to classify an aircraft in an image
1. Browse to the AWS Lambda console to create a new function: https://console.aws.amazon.com/lambda/home#/create
2. Select the **Author from Scratch** option:
3. Fill out the following information for the Lambda function:
* Name: **mlbot-classify**
* Runtime: **Python 3.7**
* Permissions: **Expand: Choose or create an execution role**
4. Specify the following information for Execution role:
* **Create a new role with basic Lambda permissions**
* A Role Name will be created containing: **mlbot-classify** name as prefix, the role name looks like mlbot-classify2-role-le0fretk
5. Click the **Create** function' button
6. Replace the existing Lambda function code with the following.
```
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
```
7. Add an environment variable named **EndpointName** and provide the name of your SageMaker endpoint.
7. Click the **Save** button to finish

## Task 5: Test the Lambda function
Create a test event and test your Lambda function 
1. Browse to the AWS Lambda console to edit the **mlbot-classify** Lambda function: https://console.aws.amazon.com/lambda/home#/functions/mlbot-classify
2. Click on the **Select a test event..** drop down and select **Configure test events**
3. Specify the following information for the test event:
* Event template: **Hello World**
* Event name: **mlbot**
* Code:
```
{
  "url": "https://github.com/AwsGeek/mlbot-hamburg/raw/master/lab5/airbus-a320.jpg"
}
```
4. Click on the **Create** button to continue
5. Click click on the **Test** button to verify operation of your Lambda function and invocation of your SageMaker endpoint.

What result do you get?

## Task 6: Update the IAM role
Update the IAM role to allow invocation of the SageMaker InvokeEndpoint API
1. In **mlbot-classify** Lambda function scroll down to **Execution role** pane and click on **View the mlbot-classify2-role-<id> role** to go the IAM role page.
2. Click on the **Add inline policy** button
3. Click on the **JSON** tab and replace the existing policy with the following. Replace ```<SageMaker Endpoint ARN>``` with the name of your SageMaker Endpoint ARN.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "mlbot",
            "Effect": "Allow",
            "Action": "sagemaker:InvokeEndpoint",
            "Resource": "<SageMaker Endpoint ARN>"
        }
    ]
}
```
4. Click on the **Review policy** button to continue
5. Name the policy **mlbot-classify**, then click on the **Create policy** button to finish

## Task 7: Test the Lambda function (again)
1. Browse to the AWS Lambda console to edit the **mlbot-classify** Lambda function: https://console.aws.amazon.com/lambda/home#/functions/mlbot-classify
2. Click click on the **Test** button to verify operation of your Lambda function and invocation of your SageMaker endpoint.

What result do you get this time?
