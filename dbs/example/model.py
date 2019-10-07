# coding:utf-8

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from driver.databases.mysql import ModelDict

Base = declarative_base()


class ExampleTable(Base, ModelDict):
    __tablename__ = 'example'

    id = Column(String(36), primary_key=True)
    name = Column(String(64))
    task_id = Column(String(36), default="unknow")
    created_time = Column(DateTime, default=datetime.now)
    updated_time = Column(DateTime, default=datetime.now)


