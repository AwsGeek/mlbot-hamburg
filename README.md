# Build a Serverless Machine Learning Bot
<p align="center"><img src="https://www.awsgeek.com/hamburg19/boeing-747.jpg"></p>

## Overview
In this tutorial, you will build a serverless bot using Slack and Amazon Web Services, including AWS Lambda, Amazon SageMaker, SQS, and API Gateway. The bot will help you classify commercial aircraft found in images. 
### Objectives
In this tutorial you will perform the following tasks:

* **[Aircraft classifier](AircraftClassifier)** -
In this lab you will use Amazon SageMaker to train an aircraft classification model and AWS Lambda to build an interface for your Amazon SageMaker endpoint.

* **[Aircraft detector](AircraftDetector)** -
In this lab you will use Amazon Rekognition to detect aircraft and create and AWS Lambda to interact with Rekognition.

* **[Request handler](RequestHandler)** -
In this lab you will use AWS Lambda and SQS to queue and process classification requests

* **[Slack bot](SlackBot)** -
In this lab you will create a Slack bot that allows you to send request to your aircraft classify

* **[Request dispatcher](RequestDispatcher)** -
In this lab you will use Amazon API Gateway and AWS Lambda to create a public interface for your aircraft classifier

* **[Cleanup](Cleanup)** - 
In this lab you will tear down all AWS resources created during this tutorial.

### Prerequisites
* AWS account
* Slack account

_**Note:** For this tutorial you will be creating and using AWS resources including Amazon S3, SageMaker, Lambda, SQS, and API Gateway. All AWS resources must be created in the same AWS region._

_For an up-to-date list of services and supported regions, see https://docs.aws.amazon.com/general/latest/gr/rande.html_
