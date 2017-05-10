# -*- coding: utf-8 -*-
# __author__: taohu

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

from sqlalchemy import create_engine, ForeignKey, Column
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.types import String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
from generate import DBConfig

# 创建 engine , isolation_level="READ UNCOMMITTED": 否则无法实时读取 db 中已变更的数据, https://www.v2ex.com/t/198981
engine = create_engine(DBConfig.SQLALCHEMY_DATABASE_URI, pool_recycle=7200, isolation_level="READ UNCOMMITTED")
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    memo = Column(String(50), unique=True, nullable=False)
    type = Column(String(50), nullable=False)
    # info_list = relationship('Info', order_by='Info.id', lazy="dynamic")


class Info(Base):
    __tablename__ = 'info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(String(50), server_default='', nullable=False)
    port = Column(String(8), server_default='', nullable=False)
    db_name = Column(String(50), server_default='', nullable=False)
    size = Column(String(50), server_default='', nullable=False)
    tactics = Column(String(8), nullable=False)
    agent_date = Column(String(16), server_default=datetime.datetime.now().strftime('%Y-%m-%d'), nullable=False)
    ctime = Column(DateTime, index=True, default=datetime.datetime.now, nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), index=True, nullable=False)
    project_obj = relationship('Project', lazy='joined', cascade='all')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
