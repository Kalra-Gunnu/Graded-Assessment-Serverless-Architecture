# Graded-Assessment-Serverless-Architecture

## Table of Contents

- [Assignment 1 - 🔁 EC2 Automation](#assignment-1---automated-ec2-instance-management-using-aws-lambda-and-boto3)
- [Assignment 8 - 🧠 Sentiment Analysis](#assignment-8---sentiment-analysis-of-user-reviews-using-aws-lambda-and-amazon-comprehend)
- [Assignment 11 - ☁️ EC2 Backup with Lambda](#assignment-11---ec2-backup-and-cleanup-with-lambda-s3-and-eventbridge)
- [Assignment 12 - 🚀 Auto-Scale with ALB](#assignment-12---auto-scale-ec2-instances-based-on-alb-load-using-aws-lambda)


## Assignment 1 - Automated EC2 Instance Management using AWS Lambda and Boto3

### 📌 Objective

- This assignment demonstrates how to:
    - Automatically manage EC2 instance power states
    - Stop instances tagged as `Auto-Stop`
    - Start instances tagged as `Auto-Start`
    - Limit to instances owned by me (`Name` tag starts with `gun-assignment-*`)

### 🔧 Steps

1. 🚀 Launching EC2 Instances

    1. Opened AWS EC2 Dashboard
    2. Launched 2 t2.micro instances
    3. Added the tag `Auto-Stop` to Instance_1(`gun-assignment-1`) and `Auto-Start` to Instance_2(`gun-assignment-2`)
    4. Screenshot 1 & 2

2. 🔐 Creating IAM Role for Lambda

    1. Went to IAM > Roles > Create Role
    2. Selected `AWS service` as the trusted service and use case as `Lambda`
    3. Attached the below policy
        - `AmazonEC2FullAccess` -> Provides full access to Amazon EC2 via the AWS Management Console
    4. Named it: `GunLambdaEC2ControlRole`
    5. Screenshot 3 & 4

3. 📦 Creating Lambda Function

    1. Opened AWS Lambda > Create Function
    2. Selected:
        - Runtime: `Python 3.13`
        - Use existing role: `GunLambdaEC2ControlRole`
    3. Named it `GunLambdaForEC2Automate`    
    4. In the code section added the code as per [lambda_function.py](Assignment_1/lambda_function.py)
    5. Deployed the function
    6. Screenshot 5 & 6

4. ⚙️ Configuring Lambda Timeout(As the default is only 3 seconds which is not sufficient)

    1. Went to Configuration > General configuration
    2. Clicked Edit
        - Set Timeout to at least 30 seconds
    3. Saved the configuration
    4. Screenshot 7

5. 🧪 Testing the Setup

    1. Went to Test > Create test event (use {} for input)
    2. Tested it 3 times:
        - With both running: After running, Stopped the 1st instance
        - With both stopped: After running, Started the 2nd instance
        - With 1st running and 2nd stopped: After running, Stopped 1st instance and Started 2nd instance
    3. Screenshot 8 through 17

## Assignment 8 - Sentiment Analysis of User Reviews using AWS Lambda and Amazon Comprehend

### 📌 Objective

- This assignment demonstrates how to:
    - Deploy a Lambda function using Python and Boto3.
    - Use Amazon Comprehend to analyze sentiments (Positive, Negative, Neutral, Mixed).

### 🔧 Steps

1. 🔐 Creating IAM Role for Lambda

    1. Went to AWS Console → IAM → Roles → Create Role.
    2. Selected `AWS service` as the trusted service and use case as `Lambda`
    3. Attached the following policies:
        - `ComprehendFullAccess` -> Provides full access to Amazon Comprehend
        - `AWSLambdaBasicExecutionRole` -> Provides write permissions to CloudWatch Logs
    4. Named it: `GunLambdaComprehend`
    5. Screenshot 1 through 3

2. 📦 Creating Lambda Function

    1. Opened AWS Lambda → Create Function
    2. Selected:
        - Runtime: `Python 3.13`
        - Execution role: Use existing role → `GunLambdaComprehend`
    3. Named it `GunAnalyseSentimentsLambda`
    4. In the code section added the code as per [lambda_function.py](Assignment_8/lambda_function.py)
    5. Deployed the function.
    6. Screenshot 4 & 5

3. ⚙️ Configuring Lambda Timeout(As the default is only 3 seconds which is not sufficient)

    1. Go to Configuration > General configuration
    2. Click Edit
        - Set Timeout to at least 30 seconds
    3. Save the configuration
    4. Screenshot 6

5. 🧪 Testing the Setup

    1. Went to Test > Create test event
    2. Used the input as 
        ```json
            {
            "reviews": [
                "The product quality is outstanding and delivery was quick!",
                "Terrible experience, never buying again.",
                "Average service, nothing special.",
                "Absolutely love it! Five stars!"
            ]
            }
        ```
    3. Clicked Test
    4. Got the below output
         ```json
            {
            "statusCode": 200,
            "body": "[{\"review\": \"The product quality is outstanding and delivery was quick!\", \"sentiment\": \"POSITIVE\", \"scores\": {\"Positive\": 0.9998030066490173, \"Negative\": 2.6848219931707717e-05, \"Neutral\": 0.00014002130774315447, \"Mixed\": 3.01614600175526e-05}}, {\"review\": \"Terrible experience, never buying again.\", \"sentiment\": \"NEGATIVE\", \"scores\": {\"Positive\": 5.5882537708384916e-05, \"Negative\": 0.9998699426651001, \"Neutral\": 3.552652196958661e-05, \"Mixed\": 3.859693606500514e-05}}, {\"review\": \"Average service, nothing special.\", \"sentiment\": \"NEGATIVE\", \"scores\": {\"Positive\": 0.04296882823109627, \"Negative\": 0.7299136519432068, \"Neutral\": 0.009315179660916328, \"Mixed\": 0.21780230104923248}}, {\"review\": \"Absolutely love it! Five stars!\", \"sentiment\": \"POSITIVE\", \"scores\": {\"Positive\": 0.999737560749054, \"Negative\": 8.89741349965334e-05, \"Neutral\": 0.00012599884939845651, \"Mixed\": 4.741360680782236e-05}}]"
            }
        ```
    5. Screenshot 7 & 8

## Assignment 11 - EC2 Backup and Cleanup with Lambda, S3 and EventBridge

### 📌 Objective

-  This project automatically backs up specified directories from an EC2 instance to an S3 bucket using AWS Lambda and deletes backups older than 30 days.

### 🔧 Steps

1. 🔐 Creating IAM Role for Lambda

    1. Went to AWS Console → IAM → Roles → Create Role.
    2. Selected `AWS service` as the trusted service and use case as `Lambda`
    3. Attached the following policies:
        - `AWSLambdaBasicExecutionRole` -> Provides write permissions to CloudWatch Logs
        - `AmazonSSMFullAccess` -> Provides full access to Amazon SSM
        - `AmazonS3FullAccess` -> Provides full access to all buckets via the AWS Management Console
    4. Named it: `GunBackupRole`
    5. Screenshot 1 & 2

2. 🚀 Launching EC2 Instances

    1. Opened AWS EC2 Dashboard
    2. Launched an ubuntu t2.micro instance
    3. Screenshot 3

3. 🔐 Creating IAM Role for EC2 and attaching to EC2 instance

    1. Went to AWS Console → IAM → Roles → Create Role.
    2. Selected `AWS service` as the trusted service and use case as `EC2`
    3. Attached the following policies:
        - `AmazonSSMManagedInstanceCore` -> The policy for Amazon EC2 Role to enable AWS Systems Manager service core functionality
        - `AmazonS3FullAccess` -> Provides full access to all buckets via the AWS Management Console
    4. Named it: `GunEC2SSMRole`
    5. Attached the above role to my EC2 Instance
        - Went to EC2 -> Instances
        - Selected my instance → Actions > Security > Modify IAM Role
        - Selected the Role `GunEC2SSMRole` and clicked on `Update IAM Role`
    6. Screenshot 4 & 5


4. ⚙️ 🛠️ Installing Required Tools and folder on EC2:

    1. Ran below commands
    ```bash
        # 1. Update packages
        sudo apt update

        # 2. Install required tools
        sudo apt install -y unzip curl

        # 3. Download the AWS CLI v2 installer
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

        # 4. Unzip the package
        unzip awscliv2.zip

        # 5. Install AWS CLI
        sudo ./aws/install

        # 6. Verify the installation
        aws --version

        # 7. Install ZIP
        sudo apt install -y zip

        # 8. Make a data folder in /home/ubuntu
        mkdir -p /home/ubuntu/data

        # 9. Create a test file inside data folder
        sudo nano /home/ubuntu/data/sample.txt

        # 10. Give the below content in the file
        sample text
    ```
    2. Screenshots 6 through 9

5. 📦 Create S3 Bucket

    1. Went to Amazon S3 -> Buckets -> Create Bucket
    2. Parameters:
        - Bucket Type: `General purpose`
        - Bucket name: `gundeep-ec2-backup-bucket`
    3. Clicked on Create folder and created a `backups/` inside the S3 bucket
    4. Screenshots 10 & 11

6. 📦 Creating Lambda Function

    1. Opened AWS Lambda → Create Function
    2. Selected:
        - Runtime: `Python 3.13`
        - Execution role: Use existing role → `GunBackupRole`
    3. Named it `gundeepEC2BackupLambda`    
    4. In the code section added the code as per [lambda_function.py](Assignment_11/lambda_function.py)
    5. Deployed the function.
    6. Screenshot 12 & 13


7. ⏰ Schedule Lambda with EventBridge

    1. Rule Details:
        - Name: `GunEC2DailyBckup`
        - Type: `Schedule`
    2. Creating Schedule
        - Pattern: `Recurring Schedule`
        - Type: `Rate-based schedule`
        - Rate expression: `rate(1 day)`
    3. Selecting Target:  
        - Select Lambda
        - Lambda Function: `gundeepEC2BackupLambda`
    4. Screenshots 14 through 18


8. 🧪 Testing the setup & Validation
    1. Manual Trigger:
        - Went to my Lambda
        - Clicked Test
        - Created a test event with {} as the payload
    2. Verification:
        - See the logs in lambda function console for the run and see the success for the run
        - Checked the Cloudwatch Log streams and see the success for all the steps
        - a new .zip file appears in /tmp location of the EC2 instance
        - New zip file appears in backups/ folder of the S3 bucket
    3. Screenshots 19 through 22
    4. For testing purpose, changed my code to delete backup after 3 hours by modifying below command:
        - FROM: 
        ```bash 
        threshold = datetime.now(timezone.utc) - timedelta(days=30)
        ```
        - TO:
        ```bash 
        threshold = datetime.now(timezone.utc) - timedelta(hours=3)
        ```
    5. This deleted the old backup created more than 3 hours ago and created a fresh new one.
    6. Screenshots 23 through 25

## Assignment 12 - Auto-Scale EC2 Instances Based on ALB Load Using AWS Lambda

### 📌 Objective

- This assignment demonstrates how to:
    - Automatically launch a new EC2 instance when the ALB receives high traffic
    - Automatically terminate an EC2 instance when traffic is low
    - Notify via SNS whenever scaling actions occur

### 🔧 Steps

1. 🔔 Creating an SNS Topic

    1. Went to SNS → Create Topic
        - Type: `Standard`
        - Name: `GunAutoScaleNotif`
    2. Clicked on Create Subscription and subscribed with my email
    3. Confirm it by going to the link on the mail received
    4. Screenshots 1 through 5

2. 🔐 Creating IAM Role for Lambda

    1. Went to AWS Console → IAM → Roles → Create Role.
    2. Selected `AWS service` as the trusted service and use case as `Lambda`
    3. Attached below 4 policies to it
        - `AmazonEC2FullAccess` -> Grants full access to Amazon EC2
        - `AmazonSNSFullAccess` -> Grants full access to Amazon Simple Notification Service (SNS)
        - `AWSLambdaBasicExecutionRole` -> Provides basic permissions for Lambda(This is essential for all Lambda functions to allow logging and troubleshooting)
        - `CloudWatchReadOnlyAccess` -> Grants read-only access to CloudWatch metrics, dashboards, logs, alarms, etc
    4. Named it: `GunAutoScalingRole`
    5. Screenshots 6 through 9

3. 📦 Creating Lambda Function

    1. Opened AWS Lambda → Create Function
    2. Selected:
        - Runtime: `Python 3.13`
        - Execution role: Use existing role → `GunAutoScalingRole`
    3. Named it `GunAutoscalerLambda`    
    4. In the code section added the code as per [lambda_function.py](Assignment_12/lambda_function.py)
    5. Deployed the function. 
    6. Screenshots 10 through 13
    7. **IMP**: Configure Lambda Timeout to 30 as the default is only 3 seconds which is not sufficient

4. ⚖️ Creating an Application Load Balancer (ALB)

    1. Went to EC2 -> Load Balancers ->  Create load balancer
        - Type: `Application Load Balancer`
    2. Named it `GunAutoScalingLB`
        - Scheme: `Internet Facing`
        - Address Type: `IPv4`
    3. Select atleast 2 Availability Zones and subnets
    4. Select `Listener: Port 80` and attach a Target Group
    5. Here I created a new TG `GunAutoScaleTargetGroup`
        - Target type: `Instances`
        - Name: `GunAutoScaleTargetGroup`
        - IP address type: `IPv4`
        - VPC: `default`
        - Protocol version: `HTTP1`
    6. Registered target EC2 instance to the TG 
    7. Screenshots 14 through 22

5. 🔁Adding the Lambda Trigger
    1. Clicked on Add Trigger in my Lambda Function
    2. Selected source as EventBridge (CloudWatch Events)
    3. Selected Create a new rule
        - Rule Name: `5minutesCheck`
        - Rule Type: `Schedule Expression`
        - Schedule Expression: `rate(5minutes)`
    4. This will run our trigger the lambda every 5 minutes
    5. Screenshot 23

6. 🛠️Setting the Environment Variables in Lambda:

    | Key                  | Value                                                  |
    |----------------------|--------------------------------------------------------|
    | `AMI_ID`             | `ami-05f991c49d264708f`                                |
    | `ELB_NAME`           | `app/GunAutoScalingLB/ea087099b3ce4f2f`                |
    | `INSTANCE_TYPE`      | `t2.micro`                                             |
    | `KEY_NAME`           | `gundeep_assignment`                                   |
    | `SECURITY_GROUP_IDS` | `sg-0db415c4a72c3d500`                                 |
    | `SNS_TOPIC_ARN`      | `arn:aws:sns:us-west-2:975050024946:GunAutoScaleNotif` |
    | `SUBNET_ID`          | `subnet-03ca36de9a927fe8e`                             |
    | `TAG_KEY`            | `Name`                                                 |
    | `TAG_VALUE`          | `GunAutoScaled`                                        |
    - Screenshot 24

7. 🧪 Testing the Setup

    1. Generated Load
        - Used [Loader.io](https://loader.io/)
        - Example: 1000 users for 1 minutes
        - Screenshot 25

    2. Monitoring Metrics
        - Went to CloudWatch → Metrics → AWS/ApplicationELB → Per AppELB Metrics
        - Looked for `RequestCount` metric on my ALB

    3. Verified Results
        - Checked Lambda logs in CloudWatch. The load was high continuously so it spawned 2 instances
        - Checked EC2 console for new/terminated instances. 2 New instances Created
        - Checked email for SNS alerts. Received 4 Notifications, first 2 for Upscaling and last 2 for downscaling
        - At last there were no instances with the TAG_VALUE `GunAutoScaled` so it just said Load is within Acceptable limits. No upscaling or downscaling needed
    4. Screenshots 26 through 38

8. 🧩 Extras To use [Loader.io](https://loader.io/)
    1. Signed Up
    2. Added my ALB uri as host
    3. Then it asked to put up a file on my server
    4. Created that file on the EC2 instance(created and attached in target group)
    5. Then installed nginx on the EC2 instance and put that file in /var/www/html
    6. Then ran the ALB uri in the Browser
    7. When the content got displayed on the browser, my ALB uri was verified as host
    8. Then created a test and tested my app for Load
