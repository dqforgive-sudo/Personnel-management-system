#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：pms -> database
@IDE    ：PyCharm
@Author ：dongqian
@Date   ：2022/3/16 22:02
@Desc   ：
=================================================='''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:520521.....dq@127.0.0.1:3306/pms" #使用pymysql作为驱动，cloud是数据库名称

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() #返回一个类，后续作为数据库模型的基类（ORM模型）
