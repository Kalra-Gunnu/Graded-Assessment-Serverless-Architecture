# Graded-Assessment-Serverless-Architecture

# ASSIGNMENT_1: 🔁 Automated EC2 Instance Management using AWS Lambda and Boto3

## 📌 Objective

Automatically manage EC2 instance power states:
    - Stop instances tagged as "Auto-Stop"
    - Start instances tagged as "Auto-Start"
    - Limit to instances owned by me ("Name" tag starts with "gun-assignment-*")

## 🔧 Steps

1. 🚀 Launch EC2 Instances

    1. Opened AWS EC2 Dashboard
    2. Launched 2 t2.micro instances
    3. Added the tag Auto_Stop to Instance_1(gun-assignment-1) and Auto_Start to Instance_2(gun-assignment-2)
    4. Screenshot 1 & 2

2. 🔐 Create IAM Role for Lambda

    1. Went to IAM > Roles > Create Role
    2. Selected "AWS service" as the trusted service and use case as "Lambda"
    3. Attached the "AmazonEC2FullAccess" policy
    4. Named it: "GunLambdaEC2ControlRole"
    5. Screenshot 3 & 4

3. 📦 Create Lambda Function

    1. Opened AWS Lambda > Create Function
    2. Selected:
        - Runtime: Python 3.13
        - Use existing role: "GunLambdaEC2ControlRole"
    3. In the code section added the code as per "lambda_function.py"
    4. Deployed the function
    5. Screenshot 5 & 6

4. ⚙️ Configure Lambda Timeout(As the default is only 3 seconds which is not sufficient)

    1. Went to Configuration > General configuration
    2. Clicked Edit
        - Set Timeout to at least 30 seconds
    3. Saved the configuration
    4. Screenshot 7

5. 🧪 Test the Function

    1. Went to Test > Create test event (use {} for input)(Screenshot 8)
    2. Clicked Test
    3. Went to EC2 Dashboard and confirm:
        - Auto-Start instance starts (if stopped)
        - Auto-Stop instance stops (if running)
    4. Tested it 3 times:
        - With both running: After running, Stopped the 1st instance(Screenshot 9, 10 & 11)
        - With both stopped: After running, Started the 2ns instance(Screenshot 12, 13, & 14)
        - With 1st running and 2nd stopped: After running, Stopped 1st instance and Started 2nd instance(Screenshot 15, 16 & 17)

# ASSIGNMENT_2:🧠 Sentiment Analysis of User Reviews using AWS Lambda & Amazon Comprehend

## 🚀 Objective

This assignment demonstrates how to:
    - Deploy a Lambda function using Python and Boto3.
    - Use Amazon Comprehend to analyze sentiments (Positive, Negative, Neutral, Mixed).

## 🔧 Steps

1. 🔐 Create IAM Role for Lambda

    1. Went to AWS Console → IAM → Roles → Create Role.
    2. Selected "AWS service" as the trusted service and use case as "Lambda"
    3. Attached the following policies:
        - "ComprehendFullAccess"
        - "AWSLambdaBasicExecutionRole"
    4. Named it: "GunLambdaComprehend"

2. 📦 Create Lambda Function

    1. Opened AWS Lambda → Create Function
    2. Selected:
        - Runtime: Python 3.13
        - Execution role: Use existing role → "GunLambdaComprehend"
    3. In the code section added the code as per "lambda_function.py"
    4. Deployed the function.

3. ⚙️ Configure Lambda Timeout(As the default is only 3 seconds which is not sufficient)

    1. Go to Configuration > General configuration
    2. Click Edit
        - Set Timeout to at least 30 seconds
    3. Save the configuration
    4. Screenshot 7

5. 🧪 Test the Function

    1. Click Test > Create test event 
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