import json
import boto3
import os
import time
from datetime import datetime

s3 = boto3.client('s3')


def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        original_key = event['Records'][0]['s3']['object']['key']

        # Download the file
        tmp_path = '/tmp/input.json'
        s3.download_file(bucket, original_key, tmp_path)

        # Validate JSON
        with open(tmp_path, 'r') as f:
            data = json.load(f)

        # Add timestamp
        epoch_ms = int(time.time() * 1000)
        filename = os.path.basename(original_key)
        new_key = f"processed/{epoch_ms}_{filename}"

        # Upload with new key
        s3.upload_file(tmp_path, bucket, new_key)

        print(f"Moved to: s3://{bucket}/{new_key}")
        return {"status": "success", "new_key": new_key}

    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error", "message": str(e)}
