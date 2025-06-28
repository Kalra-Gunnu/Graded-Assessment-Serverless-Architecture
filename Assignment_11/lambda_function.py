import boto3
import time
from datetime import datetime, timezone, timedelta

ssm = boto3.client('ssm')
s3 = boto3.client('s3')

INSTANCE_ID = 'i-0201d237a794e2dfd'  
S3_BUCKET = 'gundeep-ec2-backup-bucket'    
BACKUP_PATH = '/home/ubuntu/data'    
ZIP_PATH = '/tmp/backup.zip'
ZIP_FILE_NAME = f"backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
ZIP_S3_KEY = f"backups/{ZIP_FILE_NAME}"


def run_ssm_command(instance_id, command):
    response = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': [command]},
    )
    command_id = response['Command']['CommandId']
    time.sleep(5)  

    output = ssm.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance_id
    )

    print(f"Command: {command}")
    print(f"Status: {output['Status']}")
    print(f"StandardOutputContent:\n{output['StandardOutputContent']}")
    print(f"StandardErrorContent:\n{output['StandardErrorContent']}")

    return output


def lambda_handler(event, context):
    print("Starting EC2 backup process...")

    # 1. Confirm directory exists and list files
    print("Checking backup directory contents...")
    run_ssm_command(INSTANCE_ID, f"ls -lh {BACKUP_PATH}")

    # 2. Zip the directory
    print("Zipping backup directory...")
    zip_result = run_ssm_command(INSTANCE_ID, f"zip -r {ZIP_PATH} {BACKUP_PATH}")

    # 3. List /tmp to confirm ZIP creation
    print("Listing /tmp to confirm zip presence...")
    run_ssm_command(INSTANCE_ID, "ls -lh /tmp")

    # 4. Upload to S3
    print("Uploading zip to S3...")
    upload_result = run_ssm_command(INSTANCE_ID, f"aws s3 cp {ZIP_PATH} s3://{S3_BUCKET}/{ZIP_S3_KEY}")

    # 5. Delete old backups (>30 days)
    print("Cleaning up old backups from S3...")
    delete_old_backups()

    return {
        'statusCode': 200,
        'body': {
            'zip_status': zip_result['Status'],
            'upload_status': upload_result['Status'],
            's3_key': ZIP_S3_KEY
        }
    }


def delete_old_backups():
    threshold = datetime.now(timezone.utc) - timedelta(days=30)
    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix='backups/')
    deleted = 0

    for obj in response.get('Contents', []):
        if obj['LastModified'] < threshold:
            print(f"Deleting old backup: {obj['Key']}")
            s3.delete_object(Bucket=S3_BUCKET, Key=obj['Key'])
            deleted += 1

    print(f"Total old backups deleted: {deleted}")
