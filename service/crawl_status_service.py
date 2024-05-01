from datetime import date

import sqlalchemy
import structlog

from constants import Status, MysqlDBNames
from model.crawl_status import CrawlStatus
from repository.crawl_status_repository import CrawlStatusRepository
from settings.global_settings import CRAWL_VERSION
from utils.mysql import Mysql


class CrawlStatusService:
    def __init__(self):
        self.crawl_status_repo = CrawlStatusRepository()
        self.crawl_version = CRAWL_VERSION
        self.mysql = Mysql()
        self.db_name = MysqlDBNames.BROAD_CRAWL_DB
        self.logger = structlog.getLogger(__name__)

    def create_crawl_status_entry(self, domain, url, level, url_md5):
        try:
            self.mysql.insert(
                model_cls=CrawlStatus,
                params={
                    'url_md5': url_md5,
                    'url': url,
                    'seed_domain': domain,
                    'level': level,
                    'status': Status.STARTED.value,
                    'start_date': date.today(),
                    'crawl_version': self.crawl_version
                },
                db_name=self.db_name
            )
        except sqlalchemy.exc.IntegrityError as _:
            self.logger.error(f"crawl_status entry with url={url} already exists")

    def update_crawl_details(self, url_md5, update_args):
        self.mysql.update(model_cls=CrawlStatus, filter_args={'url_md5': url_md5}, update_dict=update_args, db_name=self.db_name)
