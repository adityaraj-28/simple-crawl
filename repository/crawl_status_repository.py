from constants import MysqlDBNames
from model.crawl_status import CrawlStatus
from utils.mysql import Mysql


class CrawlStatusRepository:
    def __init__(self):
        self.mysql = Mysql()
        self.db_name = MysqlDBNames.BROAD_CRAWL_DB

    def insert(self, params):
        self.mysql.insert(model_cls=CrawlStatus, params=params, db_name=self.db_name)
