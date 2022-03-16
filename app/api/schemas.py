#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：pms -> shcemas
@IDE    ：PyCharm
@Author ：dongqian
@Date   ：2022/3/16 22:04
@Desc   ：
=================================================='''
from typing import List

from pydantic import BaseModel


class ItemBase(BaseModel):
    domain_id:int
    name: str
    domain:str
    description: str = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    domain_id: int
    domain:str
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserUp(BaseModel):
    domain: str
    name: str
    email: str
    is_active: bool

class UserUpdate(UserBase):
    is_active: bool


class User(UserBase):
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
