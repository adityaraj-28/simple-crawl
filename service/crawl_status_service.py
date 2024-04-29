from datetime import date

from constants import Status, MysqlDBNames
from model.crawl_status import CrawlStatus
from repository.crawl_status_repository import CrawlStatusRepository
from settings.global_settings import CRAWL_VERSION
from utils import calculate_md5_hash
from utils.mysql import Mysql


class CrawlStatusService:
    def __init__(self):
        self.crawl_status_repo = CrawlStatusRepository()
        self.crawl_version = CRAWL_VERSION
        self.mysql = Mysql()
        self.db_name = MysqlDBNames.BROAD_CRAWL_DB

    def create_crawl_status_entry(self, domain, url, level, url_md5):
        self.mysql.insert(
            model_cls=CrawlStatus,
            params={
                'url_md5': url_md5,
                'url': url,
                'seed_domain': domain,
                'level': level,
                'status': Status.STARTED,
                'start_date': date.today(),
                'crawl_version': self.crawl_version
            },
            db_name=self.db_name
        )

    def update_crawl_details(self, url_md5, status, redirection_chain):
        self.mysql.update(model_cls=CrawlStatus, filter_args={'url_md5': url_md5}, update_dict={
            'status': status,
            'redirection_chain': redirection_chain
        }, db_name=self.db_name)