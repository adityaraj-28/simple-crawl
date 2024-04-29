from settings.global_settings import BROAD_CRAWL_DB_CONFIG, BROAD_CRAWL_CENTRAL_DB_CONFIG, LABS_CORE_DB_CONFIG
from enum import Enum


class MysqlDBNames(Enum):
    BROAD_CRAWL_DB = BROAD_CRAWL_DB_CONFIG['db_name']
    BROAD_CRAWL_CENTRAL_DB = BROAD_CRAWL_CENTRAL_DB_CONFIG['db_name']
    LABS_CORE_DB = LABS_CORE_DB_CONFIG['db_name']


class Status(Enum):
    STARTED = 'STARTED'
    CRAWL_SUCCESS = 'CRAWL_FAILED'
    CRAWL_FAILED = 'CRAWL_FAILED'
    URL_GENERATION_FAILED = 'URL_GENERATION_FAILED'
    FILE_UPLOADED = 'FILE_UPLOADED'
