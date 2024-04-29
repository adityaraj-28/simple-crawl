from sqlalchemy import Column, Integer, String, Date, DateTime, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CrawlStatus(Base):
    __tablename__ = 'crawl_status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fingerprint = Column(String(50, collation='utf8mb4_bin'))
    url_md5 = Column(String(50, collation='utf8mb4_bin'))
    url = Column(String(1024, collation='utf8mb4_bin'))
    seed_domain = Column(String(50, collation='utf8mb4_bin'))
    level = Column(Integer)
    status = Column(String(30, collation='utf8mb4_bin'))
    start_date = Column(Date)
    crawl_version = Column(String(64, collation='utf8mb4_bin'))
    redirection_chain = Column(String(2048, collation='utf8mb4_bin'))
    s3_uri = Column(String(1024, collation='utf8mb4_bin'))
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    error_message = Column(String(1024, collation='utf8mb4_bin'))
