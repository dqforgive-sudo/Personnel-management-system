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


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(domain_id=user.domain_id, domain=user.domain, email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, domain: str, update_user: str):
    db_user_id = db.query(models.User).filter(models.User.domain == domain).first().domain_id
    user_id = db.query(models.User).filter(models.User.domain == update_user).first().domain_id
    up_user = db.query(models.Item).filter(models.Item.owner_id == db_user_id).all()
    for i in up_user:
        i.owner_id = user_id
        db.commit()
    return i


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
    user_id = db.query(models.User).filter(models.User.domain == domain).first().domain_id
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def relate_user_item(db: Session, domain: str):
    db_user = db.query(models.User).filter(models.User.domain == domain).first()
    user_id = db.query(models.User).filter(models.User.domain == domain).first().domain
    if db_item:
        db_user.domain = user_id
        db.commit()
        db.flush()
        return db.query(models.User).filter(models.User.domain == domain).first()


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
