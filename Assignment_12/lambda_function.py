import boto3
import datetime
import os

cloudwatch = boto3.client('cloudwatch')
ec2 = boto3.client('ec2')
sns = boto3.client('sns')

# Environment variables (configured in Lambda console)
ELB_NAME = os.environ['ELB_NAME'] 
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']
AMI_ID = os.environ['AMI_ID']
INSTANCE_TYPE = os.environ['INSTANCE_TYPE']
KEY_NAME = os.environ['KEY_NAME']
# SECURITY_GROUP_IDS should be a comma-separated string of security group IDs because ec2.run instances expects a list. You can give a single security group as input though
SECURITY_GROUP_IDS = os.environ['SECURITY_GROUP_IDS'].split(',') 
SUBNET_ID = os.environ['SUBNET_ID']
TAG_KEY = os.environ['TAG_KEY']
TAG_VALUE = os.environ['TAG_VALUE']

# Thresholds for scaling decisions
HIGH_THRESHOLD = 1000  # Total requests over 5 minutes to scale up
LOW_THRESHOLD = 200    # Total requests to scale down

def lambda_handler(event, context):
    """
    AWS Lambda Function: Auto-Scale EC2 Instances Based on ALB RequestCount

    Algorithm & Working:
    1. Fetch the sum of incoming requests from CloudWatch for the past 5 minutes
       using the 'RequestCount' metric from the specified Application Load Balancer.
    2. List all running EC2 instances tagged with a specific autoscaling tag.
    3. If traffic is high (above HIGH_THRESHOLD):
       - Launch a new EC2 instance with required settings (AMI, instance type, security groups).
       - Tag it appropriately and notify via SNS.
    4. If traffic is low (below LOW_THRESHOLD) and there are running instances:
       - Terminate one of the tagged running instances.
       - Notify via SNS.
    5. If traffic is within limits, no scaling action is taken.

    Purpose:
    Enables basic auto-scaling for EC2 instances based on load balancer traffic, with real-time
    notifications via SNS. Helps maintain performance and cost-efficiency without manual intervention.
    """

    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(minutes=5)
    
    # Fetch RequestCount from CloudWatch1
    try:
        metrics = cloudwatch.get_metric_statistics(
            Namespace='AWS/ApplicationELB',
            MetricName='RequestCount',
            Dimensions=[
                {'Name': 'LoadBalancer', 'Value': ELB_NAME}
            ],
            StartTime=start_time,
            EndTime=now,
            Period=300,
            Statistics=['Sum']
        )
    except Exception as e:
        print(f"Error fetching metrics: {e}")
        return

    if not metrics['Datapoints']:
        print("No datapoints found")
        return

    request_count = metrics['Datapoints'][0]['Sum']
    print(f"RequestCount (last 5 mins): {request_count}")

    # List instances tagged with your autoscaling tag
    response = ec2.describe_instances(
        Filters=[{
            'Name': f'tag:{TAG_KEY}',
            'Values': [TAG_VALUE]
        }]
    )
    instances = [
        i['InstanceId']
        for r in response['Reservations']
        for i in r['Instances']
        if i['State']['Name'] == 'running'
    ]

    if request_count > HIGH_THRESHOLD:
        # Scale up: Launch new EC2 instance
        new_instance = ec2.run_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            KeyName=KEY_NAME,
            SecurityGroupIds=SECURITY_GROUP_IDS,
            SubnetId=SUBNET_ID,
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': TAG_KEY, 'Value': TAG_VALUE}]
            }]
        )
        instance_id = new_instance['Instances'][0]['InstanceId']
        message = f"High load detected: {request_count} requests. Launched instance: {instance_id}"
        sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message)
        print(message)

    elif request_count < LOW_THRESHOLD and instances:
        # Scale down: Terminate one EC2 instance
        instance_to_terminate = instances[0]
        ec2.terminate_instances(InstanceIds=[instance_to_terminate])
        message = f"Low load detected: {request_count} requests. Terminated instance: {instance_to_terminate}"
        sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message)
        print(message)

    else:
        print("Load is within acceptable limits.")
