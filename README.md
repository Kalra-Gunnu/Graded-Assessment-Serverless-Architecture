# Graded-Assessment-Serverless-Architecture

# ASSIGNMENT_1: 🔁 Automated EC2 Instance Management using AWS Lambda and Boto3

## 📌 Objective

- This assignment demonstrates how to:
    - Automatically manage EC2 instance power states
    - Stop instances tagged as "Auto-Stop"
    - Start instances tagged as "Auto-Start"
    - Limit to instances owned by me ("Name" tag starts with "gun-assignment-*")

## 🔧 Steps

1. 🚀 Launching EC2 Instances

    1. Opened AWS EC2 Dashboard
    2. Launched 2 t2.micro instances
    3. Added the tag Auto_Stop to Instance_1(gun-assignment-1) and Auto_Start to Instance_2(gun-assignment-2)
    4. Screenshot 1 & 2

2. 🔐 Creating IAM Role for Lambda

    1. Went to IAM > Roles > Create Role
    2. Selected "AWS service" as the trusted service and use case as "Lambda"
    3. Attached the "AmazonEC2FullAccess" policy
    4. Named it: "GunLambdaEC2ControlRole"
    5. Screenshot 3 & 4

3. 📦 Creating Lambda Function

    1. Opened AWS Lambda > Create Function
    2. Selected:
        - Runtime: Python 3.13
        - Use existing role: "GunLambdaEC2ControlRole"
    3. In the code section added the code as per "lambda_function.py"
    4. Deployed the function
    5. Screenshot 5 & 6

4. ⚙️ Configuring Lambda Timeout(As the default is only 3 seconds which is not sufficient)

    1. Went to Configuration > General configuration
    2. Clicked Edit
        - Set Timeout to at least 30 seconds
    3. Saved the configuration
    4. Screenshot 7

5. 🧪 Testing the Setup

    1. Went to Test > Create test event (use {} for input)
    2. Clicked Test
    3. Went to EC2 Dashboard and confirm:
        - Auto-Start instance starts (if stopped)
        - Auto-Stop instance stops (if running)
    4. Tested it 3 times:
        - With both running: After running, Stopped the 1st instance
        - With both stopped: After running, Started the 2ns instance
        - With 1st running and 2nd stopped: After running, Stopped 1st instance and Started 2nd instance
    5. Screenshot 8 through 17

# ASSIGNMENT_8:🧠 Sentiment Analysis of User Reviews using AWS Lambda & Amazon Comprehend

## 📌 Objective

- This assignment demonstrates how to:
    - Deploy a Lambda function using Python and Boto3.
    - Use Amazon Comprehend to analyze sentiments (Positive, Negative, Neutral, Mixed).

## 🔧 Steps

1. 🔐 Creating IAM Role for Lambda

    1. Went to AWS Console → IAM → Roles → Create Role.
    2. Selected "AWS service" as the trusted service and use case as "Lambda"
    3. Attached the following policies:
        - "ComprehendFullAccess"
        - "AWSLambdaBasicExecutionRole"
    4. Named it: "GunLambdaComprehend"
    5. Screenshot 1 through 3

2. 📦 Creating Lambda Function

    1. Opened AWS Lambda → Create Function
    2. Selected:
        - Runtime: Python 3.13
        - Execution role: Use existing role → "GunLambdaComprehend"
    3. In the code section added the code as per "lambda_function.py"
    4. Deployed the function.
    5. Screenshot 4 & 5

3. ⚙️ Configuring Lambda Timeout(As the default is only 3 seconds which is not sufficient)

    1. Go to Configuration > General configuration
    2. Click Edit
        - Set Timeout to at least 30 seconds
    3. Save the configuration
    4. Screenshot 6

5. 🧪 Testing the Setup

    1. Went to Test > Create test event
    2. Used the input as 
        ```txt
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
         ```txt
            Response:
            {
            "statusCode": 200,
            "body": "[{\"review\": \"The product quality is outstanding and delivery was quick!\", \"sentiment\": \"POSITIVE\", \"scores\": {\"Positive\": 0.9998030066490173, \"Negative\": 2.6848219931707717e-05, \"Neutral\": 0.00014002130774315447, \"Mixed\": 3.01614600175526e-05}}, {\"review\": \"Terrible experience, never buying again.\", \"sentiment\": \"NEGATIVE\", \"scores\": {\"Positive\": 5.5882537708384916e-05, \"Negative\": 0.9998699426651001, \"Neutral\": 3.552652196958661e-05, \"Mixed\": 3.859693606500514e-05}}, {\"review\": \"Average service, nothing special.\", \"sentiment\": \"NEGATIVE\", \"scores\": {\"Positive\": 0.04296882823109627, \"Negative\": 0.7299136519432068, \"Neutral\": 0.009315179660916328, \"Mixed\": 0.21780230104923248}}, {\"review\": \"Absolutely love it! Five stars!\", \"sentiment\": \"POSITIVE\", \"scores\": {\"Positive\": 0.999737560749054, \"Negative\": 8.89741349965334e-05, \"Neutral\": 0.00012599884939845651, \"Mixed\": 4.741360680782236e-05}}]"
            }
        ```
    5. Screenshot 7 & 8

# ASSIGNMENT_12: 🚀 Auto-Scale EC2 Instances Based on ALB Load Using AWS Lambda

Demonstrates how to automatically scale EC2 instances up or down based on HTTP request load on an Application Load Balancer (ALB) using AWS Lambda, CloudWatch, Boto3, and SNS.

## 📌 Objectives

- This assignment demonstrates how to:
    - Automatically launch a new EC2 instance when the ALB receives high traffic
    - Automatically terminate an EC2 instance when traffic is low
    - Notify via SNS whenever scaling actions occur

## 🔧 Steps

1. 🔔 Creating an SNS Topic

    1. Went to SNS → Create Topic
        - Type: Standard
        - Name: "GunAutoScaleNotif"
    2. Clicked on Create Subscripton and subscribed with my email
    3. Confirm it by going to the link on the mail received
    4. Screenshots 1 through 5

2. 🔐 Creating IAM Role for Lambda

    1. Went to AWS Console → IAM → Roles → Create Role.
    2. Selected "AWS service" as the trusted service and use case as "Lambda"
    3. Attached below 4 policies to it
        - AmazonEC2FullAcces -> Grants full access to Amazon EC2
        - AmazonSNSFullAccess -> Grants full access to Amazon Simple Notification Service (SNS)
        - AWSLambdaBasicExecutionRole -> Provides basic permissions for Lambda(This is essential for all Lambda functions to allow logging and troubleshooting)
        - CloudWatchReadOnlyAccess -> Grants read-only access to CloudWatch metrics, dashboards, logs, alarms, etc
    4. Named it: "GunAutoScalingRole"
    5. Screenshots 6 through 9

3. 📦 Creating Lambda Function

    1. Opened AWS Lambda → Create Function
    2. Selected:
        - Runtime: Python 3.13
        - Execution role: Use existing role → "GunAutoScalingRole"
    3. In the code section added the code as per "lambda_function.py"
    4. Deployed the function. 
    5. Screenshots 10 through 13
    6. ***IMP***: Configure Lambda Timeout to 30 as the default is only 3 seconds which is not sufficient

4. ⚖️ Creating an Application Load Balancer (ALB)

    1. Went to EC2 -> Load Balancers ->  Create load balancer
        - Type: Application Load Balancer
    2. Named it "GunAutoScalingLB"
        - Scheme: Internet Facing
        - Address Type: IPv4
    3. Select atleast 2 Availability Zones and subnets
    4. Select Listener: Port 80 and attach a Target Group
    5. Here I created a new TG "GunAutoScaleTargetGroup"
        - Target type: Instances
        - Named: "GunAutoScaleTargetGroup"
        - IP address type: IPv4
        - VPC: default
        - Protocol version: HTTP1
    6. Registered target EC2 instance to the TG 
    7. Screenshots 14 through 22

5. 🔁Adding the Lambda Trigger
    1. Clicked on Add Trigger in my Lambda Function
    2. Selected source as EventBridge (CloudWatch Events)
    3. Selected Create a new rule
        - Rule Name: "5minutesCheck
        - Rule Type: Schedule Expression
        - Schedule Expression: rate(5minutes)
    4. This will run our trigger the lambda every 5 minutes
    5. Screenshot 23

6. 🛠️Setting the Environment Variables in Lambda:

    | Key                  | Value                                                  |
    |----------------------|--------------------------------------------------------|
    | `AMI_ID`             | `ami-05f991c49d264708f`                                |
    | `ELB_NAME`           | `app/GunAutoScalingLB/ea087099b3ce4f2f` |
    | `INSTANCE_TYPE`      | `t2.micro`                                             |
    | `KEY_NAME`           | `gundeep_assignment`(⚠️ No `.pem`)                    |
    | `SECURITY_GROUP_IDS` | `sg-0db415c4a72c3d500`                                 |
    | `SNS_TOPIC_ARN`      | `arn:aws:sns:us-west-2:975050024946:GunAutoScaleNotif` |
    | `SUBNET_ID`          | `subnet-03ca36de9a927fe8e`                             |
    | `TAG_KEY`            | `Name`                                                 |
    | `TAG_VALUE`          | `GunAutoScaled`                                        |
    - Screenshot 24

7. 🧪 Testing the Setup

    1. Generated Load
        - Used Loader.io(https://loader.io/)
        - Example: 1000 users for 1 minutes
        - Screenshot 25

    2. Monitoring Metrics
        - Went to CloudWatch → Metrics → AWS/ApplicationELB → Per AppELB Metrics
        - Looked for `RequestCount` metric on my ALB

    3. Verified Results
        - Checked Lambda logs in CloudWatch. The load was high continously so it spawned 2 instances
        - Checked EC2 console for new/terminated instances. 2 New instances Created
        - Checked email for SNS alerts. Received 4 Notifications, first 2 for Upscaling and last 2 for downscaling
        - At last there were no instances with the TAG_VALUE "GunAutoScaled" so it just said Load is within Acceptable limits. No upscalinjg or downscaling needed
    4. Screenshots 26 through 38
