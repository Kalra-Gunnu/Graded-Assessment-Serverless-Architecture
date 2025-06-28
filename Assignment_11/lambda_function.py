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
    """
    AWS Lambda Function: EC2 File Backup to S3 with Cleanup

    Algorithm & Working:
    1. Use AWS Systems Manager (SSM) to run shell commands on an EC2 instance.
    2. Check if the backup directory exists and list its contents.
    3. Create a ZIP file of the directory and store it in the /tmp path.
    4. Verify ZIP file creation by listing the /tmp directory.
    5. Upload the ZIP file to a designated S3 bucket under the 'backups/' prefix.
    6. Call `delete_old_backups()` to remove ZIPs older than 30 days from S3.

    Purpose:
    Automates backup of files from an EC2 instance to S3, while maintaining storage hygiene
    by deleting old backups older than 30 days. Helps in scheduled and cost-effective snapshot-style backups.
    """

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
