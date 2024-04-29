from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Proxy(Base):
    __tablename__ = 'proxies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean)
    bad_proxy = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    ip_address = Column(String(191, collation='utf8mb4_bin'))
    password = Column(String(191, collation='utf8mb4_bin'))
    port = Column(String(191, collation='utf8mb4_bin'))
    updated_at = Column(DateTime, nullable=False)
    username = Column(String(191, collation='utf8mb4_bin'))