# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, DateTime,String,BINARY
from grouptime.database import Base
from datetime import datetime, timedelta
from flask_login import UserMixin

from hashlib import pbkdf2_hmac
from os import urandom

#userのモデル（id=int,名前=str,ハッシュ化されたパスワード=バイナリ配列,ハッシュ化するときのsalt=バイナリ配列）
class User(Base,UserMixin):
    __tablename__="users"
    id =Column(Integer,primary_key=True,autoincrement=True,unique=True)
    name = Column(String(64),default='user'+id)
    hash_passwd=Column(BINARY(32),nullable=False)
    salt=Column(BINARY(64),nullable=False)

    def __init__(self, name, passwd):
        self.name=name
        self.salt = urandom(64)
        self.hash_passwd=pbkdf2_hmac('sha256',passwd.encode('utf-8'),self.salt,100000)
    
    #名前とパスワードの照会
    def is_collect(self, name,passwd):
        if name != self.name:
            return False
        return pbkdf2_hmac('sha256',passwd.encode('utf-8'),self.salt,100000) == self.hash_passwd 
        

#客のグループのモデル。(id=int,time=datetime)
class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, default=datetime.now())

    def __init__(self, id):
        self.id = id
        self.time = datetime.now()
    #終了時間は開始時の90分後
    def endtime(self):
        return self.time + timedelta(minutes=90)
    #残り時間は90分から経過時間を引いたもの
    def remtime(self):
        return 90 - (datetime.now() - self.time).seconds // 60

    def __repr__(self):
        return 'Tag id = {0} start at {1}'.format(self.id, self.time)
