import os

import dotenv
from dotenv import find_dotenv

dotenv.load_dotenv(find_dotenv())

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development').upper()
APPLICATION_TYPE = os.getenv('APPLICATION_TYPE', 'manager')
APPLICATION = os.getenv('APPLICATION', "broad-crawl")

BATCH_ID = os.getenv('BATCH_ID')

BROAD_CRAWL_DB_CONFIG = {
    'host': os.getenv('BROAD_CRAWL_DB_HOST'),
    'port': os.getenv('BROAD_CRAWL_DB_PORT'),
    'user': os.getenv('BROAD_CRAWL_DB_USER'),
    'passwd': os.getenv('BROAD_CRAWL_DB_PASSWORD'),
    'db_name': "broad_crawl_%s" % BATCH_ID
}

BROAD_CRAWL_MYSQL_ENGINE = f"mysql+pymysql://{BROAD_CRAWL_DB_CONFIG['user']}:{BROAD_CRAWL_DB_CONFIG['passwd']}" + \
                           f"@{BROAD_CRAWL_DB_CONFIG['host']}:{BROAD_CRAWL_DB_CONFIG['port']}/" + \
                           f"{BROAD_CRAWL_DB_CONFIG['db_name']}"

BROAD_CRAWL_CENTRAL_DB_CONFIG = {
    'host': os.getenv('BROAD_CRAWL_DB_HOST'),
    'port': os.getenv('BROAD_CRAWL_DB_PORT'),
    'user': os.getenv('BROAD_CRAWL_DB_USER'),
    'passwd': os.getenv('BROAD_CRAWL_DB_PASSWORD'),
    'db_name': os.getenv('BROAD_CRAWL_CENTRAL_DB_NAME')
}


BROAD_CRAWL_CENTRAL_MYSQL_ENGINE = f"mysql+pymysql://{BROAD_CRAWL_CENTRAL_DB_CONFIG['user']}:{BROAD_CRAWL_CENTRAL_DB_CONFIG['passwd']}" + \
                           f"@{BROAD_CRAWL_CENTRAL_DB_CONFIG['host']}:{BROAD_CRAWL_CENTRAL_DB_CONFIG['port']}/" + \
                           f"{BROAD_CRAWL_CENTRAL_DB_CONFIG['db_name']}"

LABS_CORE_DB_CONFIG = {
    'host': os.getenv('LABS_CORE_DB_HOST'),
    'port': os.getenv('LABS_CORE_DB_PORT'),
    'user': os.getenv('LABS_CORE_DB_USER'),
    'passwd': os.getenv('LABS_CORE_DB_PASSWORD'),
    'db_name': os.getenv('LABS_CORE_DB_NAME')
}

LABS_CORE_MYSQL_ENGINE = f"mysql+pymysql://{LABS_CORE_DB_CONFIG['user']}:{LABS_CORE_DB_CONFIG['passwd']}" + \
                    f"@{LABS_CORE_DB_CONFIG['host']}:{LABS_CORE_DB_CONFIG['port']}/{LABS_CORE_DB_CONFIG['db_name']}"

AWS_CONFIG = {
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'aws_session_token': os.getenv('AWS_SESSION_TOKEN'),
    'aws_region_id': os.getenv('AWS_REGION_ID')
}

BUCKET_NAME = os.getenv('BUCKET_NAME')
S3_PATH_PREFIX = os.getenv('S3_PATH_PREFIX', 'broad_crawl/dev')
LOCALSTACK_URL = 'http://localhost.localstack.cloud:4566'
CRAWL_VERSION = 'simple-crawl'
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36"

