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

# Task 3. Train the SageMaker model
Execute the following steps in order to train your model
1. Prepare for training. In cell 1, replace ```<replace with your bucket name>``` with the bucket name you created in a previous task, then click on the **Run** button to run this cell of the notebook.
2. Train the model. Select this cell, then click on the **Run** button to train the model. Training this model takes approximatley 5 to 10 minutes using a single ml.p3.2xlarge training instance. 
3. While waiting for the training job to finish, browse to the SageMaker console and find training job. Click on the training job and open to view details and log activity.
4. Deploy the model. Select this cell, then click on the **Run** button to deploy the model. Deploying this model can take several minutes. Note the endpoint name and ARN for later use.
5. Finally, Test the model. Select this cell, then click on the **Run** button to test the model. Verify the classification matches the displayed aircraft.

## This is the end of the lab
