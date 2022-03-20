#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：pms -> models
@IDE    ：PyCharm
@Author ：dongqian
@Date   ：2022/3/16 22:03
@Desc   ：
=================================================='''
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    domain_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    domain = Column(String(50),unique=True)
    email = Column(String(50), unique=True)
    phone = Column(String(11))
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Item(Base):
    __tablename__ = "items"

    domain_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    domain = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    phone = Column(String(11))
    is_active = Column(Boolean, default=True)
    owner_name = Column(String(100), ForeignKey("users.domain"))
    owner = relationship("User", back_populates="items")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Admin(Base):
    __tablename__ = "admin"

    admin_id = Column(Integer,primary_key=True)
    username = Column(String(50))
    passwd = Column(String(200))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Admin(Base):
    __tablename__ = "admin"

    admin_id = Column(Integer,primary_key=True)
    username = Column(String(50))
    passwd = Column(String(200))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
