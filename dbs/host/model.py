# coding:utf-8

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from driver.databases.mysql import ModelDict

Base = declarative_base()


class HostTable(Base, ModelDict):
    __tablename__ = 'host'

    id = Column(String(64), primary_key=True)
    hostname = Column(String(64))
    ipaddress = Column(String(36))
    uname = Column(String(128))
    version = Column(String(32))
    created_time = Column(DateTime, default=datetime.now)
    updated_time = Column(DateTime, default=datetime.now)


class IpaddressTable(Base, ModelDict):
    __tablename__ = 'ipaddress'

    ip = Column(String(36), primary_key=True)
    host_id = Column(String(36))
    created_time = Column(DateTime, default=datetime.now)
    updated_time = Column(DateTime, default=datetime.now)
