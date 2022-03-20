#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：pms -> crud
@IDE    ：PyCharm
@Author ：dongqian
@Date   ：2022/3/16 22:04
@Desc   ：
=================================================='''
from sqlalchemy.orm import Session

from app.api import models, schemas


def get_user(db: Session, domain: str):
    return db.query(models.User).filter(models.User.domain == domain).first()


def get_user_by_domain(db: Session, domain: str):
    return db.query(models.User).filter(models.User.domain == domain).first()

def get_item_by_domain(db: Session, domain: str):
    return db.query(models.Item).filter(models.Item.domain == domain).first()

def get_users(db: Session, page: int = 0, limit: int = 100):
    return db.query(models.User).offset(page).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(domain_id=user.domain_id, domain=user.domain, email=user.email, name=user.name,phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, domain: str,update_user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.domain == domain).first()
    if db_user:
        update_dict = update_user.dict(exclude_unset=True)
        for k, v in update_dict.items():
            setattr(db_user, k, v)
        db.commit()
        db.flush()
        db.refresh(db_user)
        return db_user


def delete_user(db: Session, domain: str):
    db_user = db.query(models.User).filter(models.User.domain == domain).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        db.flush()
        return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, domain: str):
    user_domain = db.query(models.User).filter(models.User.domain == domain).first().domain
    db_item = models.Item(**item.dict(), owner_name=user_domain)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def relate_user_item(db: Session, domain: str,ndomain:str):
    db_user = db.query(models.Item).filter(models.Item.owner_name == domain).all()
    user_id = db.query(models.User).filter(models.User.domain == ndomain).first()
    if user_id:
        for i in db_user:
            i.owner_name = ndomain
            db.commit()
        db.flush()
        return db.query(models.User).filter(models.User.domain == ndomain).first()

def create_item(db: Session, user: schemas.ItemCreate):
    db_user = models.Item(domain_id=user.domain_id, domain=user.domain, email=user.email, name=user.name,phone=user.phone,owner_name=user.owner_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_item(db: Session, domain: str, update_item: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.domain == domain).first()
    if db_item:
        update_dict = update_item.dict(exclude_unset=True)
        for k, v in update_dict.items():
            setattr(db_item, k, v)
        db.commit()
        db.flush()
        db.refresh(db_item)
        return db_item


def delete_item(db: Session, domain: str):
    db_item = db.query(models.Item).filter(models.Item.domain == domain).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        db.flush()
        return db_item

def vality_admin(db:Session,admin_info:schemas.Admin):
    db_info = db.query(models.Admin).filter(models.Admin.username == admin_info.username,models.Admin.passwd ==admin_info.passwd).first()
    if db_info:
        return db_info

def vality_admin(db:Session,admin_info:schemas.Admin):
    db_info = db.query(models.Admin).filter(models.Admin.username == admin_info.username,models.Admin.passwd ==admin_info.passwd).first()
    if db_info:
        return db_info
