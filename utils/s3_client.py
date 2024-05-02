import os
import uuid
from datetime import date

import boto3
import structlog

from settings.global_settings import AWS_CONFIG, ENVIRONMENT, BUCKET_NAME, LOCALSTACK_URL, CRAWL_VERSION, S3_PATH_PREFIX


class S3Client:
    def __init__(self):
        if ENVIRONMENT.lower() == 'dev':
            self.s3 = boto3.client(
                's3',
                endpoint_url=LOCALSTACK_URL
            )
        else:
            self.s3 = boto3.client('s3')
        self.bucket_name = BUCKET_NAME
        self.crawl_version = CRAWL_VERSION
        self.logger = structlog.getLogger(__name__)

    def upload_to_s3(self, domain, data):
        filename = f"{uuid.uuid4()}.html"
        start_date = date.today()
        s3_key = f"{S3_PATH_PREFIX}/{domain}/{start_date}/{filename}"
        s3_path = f"s3://{self.bucket_name}/{s3_key}"
        self.logger.info(f"uploading to s3 bucket = {self.bucket_name}, s3_path = {s3_path}")
        self.s3.put_object(Bucket=self.bucket_name, Key=s3_key, Body=data)
        return f"s3://{self.bucket_name}/{s3_key}"

