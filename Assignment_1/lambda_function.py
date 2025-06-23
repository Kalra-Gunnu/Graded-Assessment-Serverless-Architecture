import boto3

def lambda_handler(event, context):
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
    
    to_start = []
    to_stop = []

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            action = tags.get('Action')
            name = tags.get('Name', '')

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
