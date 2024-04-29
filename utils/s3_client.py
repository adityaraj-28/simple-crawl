import os

import boto3
import structlog

from settings.global_settings import AWS_CONFIG, ENVIRONMENT, BUCKET_NAME, LOCALSTACK_URL, CRAWL_VERSION, S3_PATH_PREFIX


class S3Client:
    def __init__(self):
        if ENVIRONMENT == 'dev':
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=AWS_CONFIG['aws_access_key_id'],
                aws_secret_access_key=AWS_CONFIG['aws_secret_access_key'],
                aws_session_token=AWS_CONFIG['aws_session_token'],
                region_name=AWS_CONFIG['aws_region_id'],
                endpoint_url=LOCALSTACK_URL
            )
        else:
            self.s3 = boto3.client('s3')
        self.bucket_name = BUCKET_NAME
        self.crawl_version = CRAWL_VERSION
        self.logger = structlog.getLogger(__name__)

    def uploadToS3(self, domain, filepath, filename):
        filepath = os.path.join(filepath, filename)
        start_date = self.crawl_version[0:8]
        s3_key = f"{S3_PATH_PREFIX}/{domain}/{start_date}/{filename}"
        self.logger.info(f"uploading to s3 filepath= {filepath}, bucket = {self.bucket_name}, s3_key = {s3_key}")
        self.s3.upload_file(filepath, self.bucket_name, s3_key)
        return f"s3://{self.bucket_name}/{s3_key}"

    def uploadOnboardingToS3(self, filepath, filename):
        filepath = os.path.join(filepath, filename)
        s3_key = f"{S3_PATH_PREFIX}/onboarding/{filename}"
        self.logger.info(f"uploading to s3 filepath= {filepath}, bucket = {self.bucket_name}, s3_key = {s3_key}")
        self.s3.upload_file(filepath, self.bucket_name, s3_key)
        return s3_key

    def s3_folder_path(self, domain, start_date):
        s3_key = f"broad_crawl/{domain}/{start_date}/"
        return f"s3://{self.bucket_name}/{s3_key}"

    def list_files(self, domain):
        s3_key = f"broad_crawl/{domain}/"
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=s3_key)
        file_s3_keys = []
        for obj in response.get('Contents', []):
            file_s3_keys.append(obj['Key'])
        return file_s3_keys

    def file_content(self, file_key):
        obj = self.s3.get_object(Bucket=self.bucket_name, Key=file_key)
        data = obj['Body'].read()
        return data

    @staticmethod
    def extract_file_key(s3_path):
        if s3_path.startswith('s3://'):
            s3_path = s3_path[len('s3://'):]
        components = s3_path.split('/')
        file_key = '/'.join(components[1:])
        return file_key
