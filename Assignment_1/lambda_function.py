# Importing necessary libraries
import boto3

def lambda_handler(event, context):
    """
    AWS Lambda Function: Auto-Start/Stop EC2 Instances Based on Tags

    Algorithm & Working:
    1. Initialize EC2 client using Boto3.
    2. Filter EC2 instances that:
       - Have a 'tag:Action' with value 'Auto-Start' or 'Auto-Stop'.
       - Have a 'tag:Name' that starts with 'gun-assignment-*'.
    3. Check instance state:
       - If Action is 'Auto-Start' and instance is not running → add to start list.
       - If Action is 'Auto-Stop' and instance is not stopped → add to stop list.
    4. Start or stop the instances using start_instances() or stop_instances().

    Purpose:
    Automatically manage EC2 instance lifecycle based on user-defined tags.
    """

    # Initialize the EC2 client
    ec2 = boto3.client('ec2')
    
    # Describe instances with both Action and Name tags
    instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Start', 'Auto-Stop']
            },
            {
                'Name': 'tag:Name',
                'Values': ['gun-assignment-*']
            }
        ]
    )
    # Lists to hold instance IDs for starting and stopping
    to_start = []
    to_stop = []

    # Iterate through the instances and check their tags
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            action = tags.get('Action')
            name = tags.get('Name', '')
            # Check if the instance matches the criteria for starting or stopping
            if action == 'Auto-Start' and instance['State']['Name'] != 'running':
                to_start.append(instance_id)
            elif action == 'Auto-Stop' and instance['State']['Name'] != 'stopped':
                to_stop.append(instance_id)

    # Start instances
    if to_start:
        ec2.start_instances(InstanceIds=to_start)
        print(f"Started instances: {to_start}")
    else:
        print("No instances to start.")

    # Stop instances
    if to_stop:
        ec2.stop_instances(InstanceIds=to_stop)
        print(f"Stopped instances: {to_stop}")
    else:
        print("No instances to stop.")
